# Copyright (c) 2023 Boston Dynamics, Inc.  All rights reserved. # CREDIT BOSTON DYNAMICS image_viewer.py
import argparse
import logging
import sys
import time

import cv2
import numpy as np

import bosdyn.client
import bosdyn.client.util
from bosdyn.api import image_pb2
from bosdyn.client.image import ImageClient, build_image_request
from bosdyn.client.time_sync import TimedOutError
import os

_LOGGER = logging.getLogger(__name__)

VALUE_FOR_Q_KEYSTROKE = 113
VALUE_FOR_ESC_KEYSTROKE = 27


def image_to_opencv(image, auto_rotate=True):
    """Convert an image proto message to an openCV image."""
    num_channels = 1  # Assume a default of 1 byte encodings.
    if image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_DEPTH_U16:
        dtype = np.uint16
        extension = '.png'
    else:
        dtype = np.uint8
        if image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_RGB_U8:
            num_channels = 3
        elif image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_RGBA_U8:
            num_channels = 4
        elif image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_GREYSCALE_U8:
            num_channels = 1
        elif image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_GREYSCALE_U16:
            num_channels = 1
            dtype = np.uint16
        extension = '.jpg'

    img = np.frombuffer(image.shot.image.data, dtype=dtype)
    if image.shot.image.format == image_pb2.Image.FORMAT_RAW:
        try:
            # Attempt to reshape array into a RGB rows X cols shape.
            img = img.reshape((image.shot.image.rows, image.shot.image.cols, num_channels))
        except ValueError:
            # Unable to reshape the image data, trying a regular decode.
            img = cv2.imdecode(img, -1)
    else:
        img = cv2.imdecode(img, -1)

    return img, extension


def reset_image_client(robot):
    """Recreate the ImageClient from the robot object."""
    del robot.service_clients_by_name['image']
    del robot.channels_by_authority['api.spot.robot']
    return robot.ensure_client('image')


def main(argv):
    # Parse args
    parser = argparse.ArgumentParser()
    bosdyn.client.util.add_base_arguments(parser)

    # Create robot object with an image client.
    sdk = bosdyn.client.create_standard_sdk('image_capture')
    robot = sdk.create_robot(os.environ['BOSDYN_W_IP']) # or BOSDYN_E_IP
    bosdyn.client.util.authenticate(robot)
    robot.sync_with_directory()
    robot.time_sync.wait_for_sync()

    image_client = robot.ensure_client(ImageClient.default_service_name)
    print(image_pb2.Image.PixelFormat.keys())
    # ['PIXEL_FORMAT_UNKNOWN', 'PIXEL_FORMAT_GREYSCALE_U8', 'PIXEL_FORMAT_RGB_U8', 'PIXEL_FORMAT_RGBA_U8', 'PIXEL_FORMAT_DEPTH_U16', 'PIXEL_FORMAT_GREYSCALE_U16']
    pixels = [image_pb2.Image.PixelFormat.Value('PIXEL_FORMAT_RGB_U8'),
                image_pb2.Image.PixelFormat.Value('PIXEL_FORMAT_DEPTH_U16')
    ]
    # image_sources = image_client.list_image_sources()
    # print(image_sources)
    # , name: "hand_color_image"
    # , name: "hand_color_in_hand_depth_frame"
    # , name: "hand_depth"
    # , name: "hand_depth_in_hand_color_frame"
    # , name: "hand_image"
    image_sources = ['hand_color_image', 'hand_depth_in_hand_color_frame']
    resize_ratio = 1.0
    auto_rotate = False
    requests = [
        build_image_request(image_source_name=source, quality_percent=80,
                            pixel_format=format, resize_ratio=resize_ratio) for source, format in zip(image_sources, pixels)
    ]

    disable_full_screen = False
    for image_source in image_sources:
        cv2.namedWindow(image_source, cv2.WINDOW_NORMAL)
        if len(image_sources) > 1 or disable_full_screen:
            cv2.setWindowProperty(image_source, cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_AUTOSIZE)
        else:
            cv2.setWindowProperty(image_source, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    keystroke = None
    timeout_count_before_reset = 0
    image_count = 0
    while keystroke != VALUE_FOR_Q_KEYSTROKE and keystroke != VALUE_FOR_ESC_KEYSTROKE:
        t1 = time.time()
        try:
            images_future = image_client.get_image_async(requests, timeout=0.5)
            while not images_future.done():
                keystroke = cv2.waitKey(1)
                # print(keystroke)
                if keystroke == VALUE_FOR_ESC_KEYSTROKE or keystroke == VALUE_FOR_Q_KEYSTROKE:
                    sys.exit(1)
            images = images_future.result()
        except TimedOutError as time_err:
            if timeout_count_before_reset == 5:
                # To attempt to handle bad comms and continue the live image stream, try recreating the
                # image client after having an RPC timeout 5 times.
                _LOGGER.info('Resetting image client after 5+ timeout errors.')
                image_client = reset_image_client(robot)
                timeout_count_before_reset = 0
            else:
                timeout_count_before_reset += 1
        except Exception as err:
            _LOGGER.warning(err)
            continue
        for i in range(len(images)):
            image, _ = image_to_opencv(images[i], auto_rotate)
            # Check if image is greyscale
            if image.dtype == np.uint16:
                image = image * 20
            cv2.imshow(images[i].source.name, image)
        keystroke = 1
        image_count += 1
        print(f'Mean image retrieval rate: {1/(time.time() - t1)}Hz')


if __name__ == '__main__':
    if not main(sys.argv[1:]):
        sys.exit(1)
