import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import signal


def main():
    rospy.init_node('splitter', anonymous=True)
    bridge = CvBridge()
    video_writer = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (640, 480))

    frames = []
    def callback(data):
        rgb_image = bridge.imgmsg_to_cv2(data.color, desired_encoding='passthrough')
        cv2.imshow('RGB', rgb_image)
        cv2.waitKey(1)

    rospy.Subscriber('/pose/rgbd_image', Image, callback)
    rospy.spin()

def signal_handler(signal, frame):
    video_writer.release()
    rospy.signal_shutdown("Terminated")

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()

if __name__ == '__main__':
    main()