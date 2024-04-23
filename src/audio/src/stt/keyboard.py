import rospy
from std_msgs.msg import String

def main():
    rospy.init_node("KeyboardPublisher")
    pub = rospy.Publisher("/speech/command", String, queue_size=10)
    print("Type text and press enter to publish to /speech/command")

    while not rospy.is_shutdown():
        text = input("Enter text: ")
        pub.publish(text)

if __name__ == "__main__":
    main()