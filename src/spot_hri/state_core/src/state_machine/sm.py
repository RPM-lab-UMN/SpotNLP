import rospy
from std_msgs.msg import Bool, Float32, String

def main():
    rospy.init_node('state_machine', anonymous=True)
    follow_pub = rospy.Publisher('/movement/follow', Bool, queue_size=10)
    follow_distance_pub = rospy.Publisher('/movement/follow_distance', Float32, queue_size=10)
    emote_pub = rospy.Publisher('/emote/emote', Bool, queue_size=10)
    emote_type_pub = rospy.Publisher('/emote/type', String, queue_size=10)


    state = 'idle'
    def callback(msg):
        nonlocal state
        data = msg.data.lower()
        print(f'Current state: {state}, received: {data}')
        
        if state == 'idle':
            if data == 'e':
                state = 'follow'
                follow_pub.publish(True)
                print('Follow')
            elif data == 'n':
                state = 'emote'
                emote_pub.publish(True)
                print('Emote')
        elif state == 'follow':
            if data == 'e':
                state = 'idle'
                follow_pub.publish(False)
                print('Idle')
            elif data == '1':
                follow_distance_pub.publish(1.0)
                print('Follow distance 1')
            elif data == '2':
                follow_distance_pub.publish(1.5)
                print('Follow distance 2')
            elif data == '3':
                follow_distance_pub.publish(2.0)
                print('Follow distance 3')
        elif state == 'emote':
            if data == 'n':
                state = 'idle'
                emote_pub.publish(False)
                print('Idle')
            if data == '1':
                emote_type_pub.publish('yes')
                print('Yes')
            if data == '2':
                emote_type_pub.publish('no')
                print('No')
            if data == '3':
                emote_type_pub.publish('maybe')
                print('Maybe')
            if data == 's':
                emote_type_pub.publish('sit')
                print('Sit')
            if data == 'e':
                emote_type_pub.publish('stand')
                print('Stand')

    rospy.Subscriber('/event/class', String, callback)
    rospy.spin()



if __name__ == '__main__':
    main()