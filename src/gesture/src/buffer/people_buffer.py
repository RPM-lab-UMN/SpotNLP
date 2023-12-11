import rospy
from mp_pose.msg import people, buffer
import numpy as np

# Does Record Images
def main():
    rospy.init_node('pose_buffer', anonymous=True)
    pub = rospy.Publisher('/buffer/pose', buffer, queue_size=10)
    buffer_msg = buffer()
    poses = []

    def callback(data):
        poses.append(data.people[0].pose)
        
        time = rospy.Time.now()
        while len(poses) > 0:
            diff = time - poses[0].header.stamp
            diff = diff.to_sec()
            if diff > 10:
                poses.pop(0)
            else:
                print(f'Length: {len(poses)}, Diff: {np.round(diff, 4)}')
                break
        buffer_msg.header = data.header
        buffer_msg.poses = poses
        buffer_msg.color = data.color
        buffer_msg.depth = data.depth
        buffer_msg.mask = data.people[0].image
        pub.publish(buffer_msg)
            

    rospy.Subscriber('/xmem/people', people, callback)
    rospy.spin()

if __name__ == '__main__':
    main()
