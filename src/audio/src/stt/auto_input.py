import rospy
from std_msgs.msg import String
import time

def main():
    rospy.init_node("KeyboardPublisher")
    # rospy.Subscriber('/audio/speak', String, lambda msg: print(msg.data))
    pub = rospy.Publisher("/speech/command", String, queue_size=10)
    print("Auto input starting in 1 seconds")
    time.sleep(1)

    messages = [
        "start recording",
        "save a waypoint called dogs, it has a bunch of dogs in the park",
        "stop recording and save the map",
    ]
    for message in messages:
        print(f"Sending message: {message}")
        pub.publish(message)
        time.sleep(1)

if __name__ == "__main__":
    main()