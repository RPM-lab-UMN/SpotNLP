import rospy
from mp_pose.msg import people, person, pose, landmark, depth_image, buffer
import argparse
import rosbag
import rospy
from mp_pose.msg import buffer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_name', nargs='?', default='data', help='Name of the data to save')
    args = parser.parse_args()

    rospy.init_node('pose_buffer', anonymous=True)
    bag = rosbag.Bag(f'../data/{args.data_name}.bag', 'w')

    num_messges = 0
    def callback(data):
        nonlocal num_messges
        bag.write('/buffer/pose', data)
        print(f'Recorded message {num_messges}')
        num_messges += 1

    rospy.Subscriber('/buffer/pose', buffer, callback)
    input('Press enter to stop recording')
    print(f'Stopped recording. Saved to ../data/{args.data_name}.bag')
    bag.close()

if __name__ == '__main__':
    main()
