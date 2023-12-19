import rospy
import time
import math
from mp_pose.msg import pose
from spotAPI import SpotAPI
from spotMove import SpotMove
from spotArm import SpotArm


def main():
    rospy.init_node('SpotAPI')
    local_landmarks = None
    follow = False
    follow_dist = 0.5
    def pose_callback(msg):
        nonlocal local_landmarks
        local_landmarks = msg.local_landmarks
    rospy.Subscriber('/xmem/pose', pose, pose_callback)


    spot = SpotAPI("BOSDYN_E_IP")
    move = SpotMove(spot, 1.0)
    arm = SpotArm(spot)

    arm.image_resolution('640x480')
    spot.power_on()
    move.stand()
    print('Done.')
    arm.arm_unstow()
    print('Unstowed.')
    # arm.moveL(0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 1.0)
    sh0 = 0.00
    sh1 = -2.8
    el0 = 1.5
    el1 = -0.00
    wr0 = 1.5
    wr1 = 0.0
    joints = [sh0, sh1, el0, el1, wr0, wr1]
    arm.moveJ(joints)
    arm.move_gripper(1.0)
    spot.fan_power(0, 120)
    print('Moved arm.')
    rate = rospy.Rate(100)
    start_time = time.time()
    while not rospy.is_shutdown():
        # Sin wave of seconds
        diff = time.time() - start_time
        light = (math.sin(diff*math.pi) + 1) / 2
        arm.gripper_light(True, light)

        if local_landmarks is not None:
            
            centerpoints = [11,12,23,24]
            # Get the average X and Y coordinates of the centerpoints
            x = 0
            y = 0
            for i in centerpoints:
                x += local_landmarks[i].x
                y += local_landmarks[i].y
            x /= len(centerpoints)
            y /= len(centerpoints)
            print(x, y)
            joints[0] -= (x-0.5) * 0.25
            if follow:
                pass
            else:
                arm.moveJ(joints)
            local_landmarks = None
        rate.sleep()
        

    arm.arm_stow()
    print('Stowed.')
    rospy.sleep(1)
    move.sit()



if __name__ == '__main__':
    main()
