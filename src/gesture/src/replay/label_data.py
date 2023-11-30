import rospy
import argparse
import rosbag
import rospy
import cv2
import numpy as np
import colorsys
import rospkg
import os

from dataset.write_dataset import WriteDataset

def keypoints_on_image(keypoints, image, dot_color):
    for keypoint in keypoints:
        x = int(keypoint.x * image.shape[1])
        y = int(keypoint.y * image.shape[0])
        cv2.circle(image, (x, y), 5, dot_color, -1)
    return image

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_name', nargs='?', help='Name of the data to save')
    args = parser.parse_args()

    rospy.init_node('pose_buffer', anonymous=True)
    pack_path = rospkg.RosPack().get_path('dataset')
    bag_path = os.path.join(pack_path, 'data',  f'{args.data_name}.bag')
    bag = rosbag.Bag(bag_path, 'r')
    dataset_path = os.path.join(pack_path, 'dataset_raw',  f'{args.data_name}.zarr')
    dataset = WriteDataset(dataset_path, max_history=80)

    msg_num = 0
    data = list(bag.read_messages(topics=['/buffer/pose']))

    cv2.startWindowThread()
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('frame', np.zeros((100, 100, 3), dtype=np.uint8))
    
    print("F1 to exit, Del to redo, any other key to save")
    while msg_num < len(data):
        topic, msg, t = data[msg_num]
        image = np.frombuffer(msg.color.data, dtype=np.uint8)
        image = image.reshape(msg.color.height, msg.color.width, -1)
        mask = np.frombuffer(msg.mask.data, dtype=np.uint8)
        mask = mask.reshape(msg.mask.height, msg.mask.width, -1)
        image = np.where(mask > 0, image, 0)

        num = 10
        amount = num if len(msg.poses) > num else len(msg.poses)
        offset = len(msg.poses) - amount
        for i in range(amount):
            hue = int(360 * (i / amount))
            hsv_color = colorsys.hsv_to_rgb(hue / 360, 1, 1)
            dot_color = tuple(int(255 * c) for c in hsv_color)
            image = keypoints_on_image(msg.poses[offset+i].local_landmarks, image, dot_color)

        cv2.imshow('frame', image)
        gt = cv2.waitKey(0)
        if gt == 190: # F1
            print('Exiting')
            break
        elif gt == 255: # Del
            print(f'Redoing message {msg_num-1}')
            msg_num -= 1
            dataset.remove_sample()
        else: # Any other key
            print(f'GT: {gt}, Frame: {msg_num}, Length: {len(msg.poses)}')
            # Add to dataset
            local_landmarks = np.array([np.array([np.array([keypoint.x, keypoint.y, keypoint.z, keypoint.visibility, keypoint.presence]) for keypoint in pose.local_landmarks]) for pose in msg.poses])
            world_landmarks = np.array([np.array([np.array([keypoint.x, keypoint.y, keypoint.z, keypoint.visibility, keypoint.presence]) for keypoint in pose.world_landmarks]) for pose in msg.poses])
            label = np.array([gt])
            timestamp = np.array([msg.header.stamp.to_nsec()])
            dataset.add_sample(local_landmarks, world_landmarks, label, timestamp)
            msg_num += 1
        print(np.asarray(dataset.label))
    bag.close()
    dataset.close()
    dataset.print_shapes()

if __name__ == '__main__':
    main()
