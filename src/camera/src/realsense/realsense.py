import pyrealsense2 as rs
import numpy as np
import rospy
from mp_pose.msg import depth_image
import signal
import sys

class RealSenseCamera:
    def __init__(self, width, height, fps):
        self.width = width
        self.height = height
        self.fps = fps

        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, fps)
        self.config.enable_stream(rs.stream.depth, width, height, rs.format.z16, fps)
        self.pipeline.start(self.config)

    def get_frame(self):
        frames = self.pipeline.wait_for_frames()
        align = rs.align(rs.stream.color)
        aligned_frames = align.process(frames)

        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()
        if not color_frame or not depth_frame:
            return (None, None)
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())
        return (color_image, depth_image)

    def stop(self):
        self.pipeline.stop()

if __name__ == '__main__':
    rospy.init_node('RealSenseCamera', anonymous=True)
    frame_rate = 6
    mod = 1
    camera = RealSenseCamera(640, 480,frame_rate)

    def signal_handler(signal, frame):
        camera.stop()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    pub = rospy.Publisher('/camera/rgbd_image', depth_image, queue_size=10)
    msg = depth_image()

    print('Running! Press Ctrl+C to exit:')
    num_frames = 0
    while True:
        color, depth = camera.get_frame()
        # print(type(color_image), type(depth_image))
        if color is None or depth is None:
            continue
        msg.header.stamp = rospy.Time.now()
        msg.color.height, msg.color.width = color.shape[:2]
        msg.depth.height, msg.depth.width = depth.shape[:2]
        msg.color.data = color.tobytes()
        msg.depth.data = depth.tobytes()
        msg.color.encoding = 'bgr8'
        msg.depth.encoding = '16UC1'
        msg.color.header = msg.header
        msg.depth.header = msg.header
        num_frames += 1
        if num_frames % mod == 0:
            pub.publish(msg)
        rospy.sleep(0.001)