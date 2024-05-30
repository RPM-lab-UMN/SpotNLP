import rospy
from std_msgs.msg import String
import time

def main():
    rospy.init_node("AutoPublisher")
    # rospy.Subscriber('/audio/speak', String, lambda msg: print(msg.data))
    pub = rospy.Publisher("/speech/command", String, queue_size=10)
    pub_pre = rospy.Publisher("/speech/command_pre", String, queue_size=10)
    print("Auto input starting in 1 seconds")
    time.sleep(1)

    messages = [
        "Spot, stand up",
        "Start recording",
        "Follow me",
        "This is a waypoint called the left door, it has a table next to it.",
        "This is a waypoint called TV, it has a large screen in the center of the room.",
        "This is a waypoint called the cabinet, it has a light switch next to it.",
        "Stop following and  recording.",
        # "Go to the table.",
        "Hey Spot, how many waypoints did you record?",
        "Do you have enough battery to go to the TV?",
        "Go to the waypoint with the table.",
        "Go to the TV.",
        # "Hey Spot, what is the time?",
        "Thank you Spot, you can stop now."

    ]
    for message in messages:
        print(f"Sending message: {message}")
        quit = input("Press enter to display")
        if quit is None or "":
            break
        pub_pre.publish(message)
        input("Press enter to send")
        pub.publish(message)

        # time.sleep(1)

if __name__ == "__main__":
    main()