import rospy
from std_msgs.msg import Bool, Int8, String

def main():
    rospy.init_node('state_machine', anonymous=True)
    voice_pub = rospy.Publisher('/tts/speech', String, queue_size=10)
    follow_distance_pub = rospy.Publisher('/movement/follow_distance', Int8, queue_size=10)
    follow_pub = rospy.Publisher('/movement/follow', Bool, queue_size=10)
    emote_pub = rospy.Publisher('/emote', String, queue_size=10)


    state = 'idle'
    def callback(msg):
        nonlocal state
        data = msg.data.lower()
        print(f'Current state: {state}, received: {data}')
        
        if state == 'idle':
            if data == 'e':
                state = 'follow'
                follow_pub.publish(True)
                voice_pub.publish('Now following you!')
                print('Follow')
            elif data == 'n':
                state = 'emote'
                voice_pub.publish('Emote mode!')
                print('Emote')
        elif state == 'follow':
            if data == 'e':
                state = 'idle'
                follow_pub.publish(False)
                voice_pub.publish('Stopped following you!')
                print('Idle')
            elif data == '1':
                follow_distance_pub.publish(1)
                voice_pub.publish('Follow distance 1')
                print('Follow distance 1')
            elif data == '2':
                follow_distance_pub.publish(2)
                voice_pub.publish('Follow distance 2')
                print('Follow distance 2')
            elif data == '3':
                follow_distance_pub.publish(3)
                voice_pub.publish('Follow distance 3')
                print('Follow distance 3')
        elif state == 'emote':
            if data == 'n':
                state = 'idle'
                voice_pub.publish('Exited emote mode!')
                print('Idle')
            if data == '1':
                emote_pub.publish('yes')
                voice_pub.publish('Yes')
                print('Yes')
            if data == '2':
                emote_pub.publish('no')
                voice_pub.publish('No')
                print('No')
            if data == '3':
                emote_pub.publish('maybe')
                voice_pub.publish('Maybe')
                print('Maybe')
            if data == 's':
                emote_pub.publish('sit')
                voice_pub.publish('Sit')
                print('Sit')
            if data == 'e':
                emote_pub.publish('stand')
                voice_pub.publish('Stand')
                print('Stand')

    rospy.Subscriber('/event/class', String, callback)
    rospy.spin()



if __name__ == '__main__':
    main()