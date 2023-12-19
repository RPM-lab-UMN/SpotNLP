import rospy
from mp_pose.msg import depth_image, people
from sensor_msgs.msg import Image


def main():
    rospy.init_node('splitter', anonymous=True)
    pub_d = rospy.Publisher('/pose/depth_image', Image, queue_size=10)
    pub_c = rospy.Publisher('/pose/color_image', Image, queue_size=10)
    def callback(msg):
        pub_d.publish(msg.depth)
        pub_c.publish(msg.color)
    rospy.Subscriber('/pose/rgbd_image', depth_image, callback)

    pub_mask = rospy.Publisher('/pose/mask', Image, queue_size=10)
    def callback_mask(msg):
        if msg.num_people > 0:
            pub_mask.publish(msg.people[0].image)
    rospy.Subscriber('/pose/people', people, callback_mask)
    rospy.spin()



if __name__ == '__main__':
    main()