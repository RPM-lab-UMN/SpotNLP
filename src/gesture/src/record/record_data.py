import rospy
from mp_pose.msg import people, person, pose, landmark, depth_image, buffer
import argparse
import rosbag
import rospy
import rospkg
import os
from mp_pose.msg import buffer

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('data_name', nargs='?', help='Name of the data to save')
    args = parser.parse_args()

    rospy.init_node('pose_buffer', anonymous=True)
    pack_path = rospkg.RosPack().get_path('dataset')
    bag_path = os.path.join(pack_path, 'data',  f'{args.data_name}.bag')
    bag = rosbag.Bag(bag_path, 'w')

    num_messges = 0
    def callback(data):
        nonlocal num_messges
        bag.write('/buffer/pose', data)
        print(f'Recorded message {num_messges}')
        num_messges += 1

    rospy.Subscriber('/buffer/pose', buffer, callback)
    input('Press enter to stop recording')
    print(f'Stopped recording. Saved to {bag_path}')
    bag.close()

if __name__ == '__main__':
    main()
