import rospy
from std_msgs.msg import String

def main():
    rospy.init_node('state_machine', anonymous=True)
    event_pub = rospy.Publisher('/event/class', String, queue_size=10)

    current_state = ''
    buffer = []
    def callback(msg):
        nonlocal buffer
        nonlocal current_state
        buffer.append(msg.data)
        if len(buffer) > 10:
            buffer.pop(0)
        # print(buffer)
        print(f'Class {msg.data} detected')
        classes = set(buffer)
        for cls in classes:
            if buffer.count(cls) >= 8:
                if current_state != cls:
                    current_state = cls
                    event_pub.publish(cls)
                    print(f'New state: {current_state}')
    rospy.Subscriber('/inference/class', String, callback)
    rospy.spin()

if __name__ == '__main__':
    main()