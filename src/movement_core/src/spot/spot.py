import rospy
import time
import math
import numpy as np
from mp_pose.msg import people
from spotAPI import SpotAPI
from spotMove import SpotMove
from spotArm import SpotArm

import cv2


def main():
    rospy.init_node('SpotAPI')
    local_landmarks = None
    local_image = None
    # mode = False
    mode = "follow"
    follow_dist = 1.5
    def pose_callback(msg):
        nonlocal local_landmarks
        nonlocal local_image
        local_landmarks = msg.people[0].pose.local_landmarks
        depth = msg.depth
        depth = np.frombuffer(depth.data, dtype=np.uint16)
        depth = depth.reshape(msg.depth.height, msg.depth.width, -1)
        mask = msg.people[0].image
        mask = np.frombuffer(mask.data, dtype=np.uint8)
        mask = mask.reshape(msg.people[0].image.height, msg.people[0].image.width, -1)
        depth = np.where(mask > 0, depth, 0)
        depth = depth[:,:,0]
        local_image = depth
    rospy.Subscriber('/xmem/people', people, pose_callback)


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

        if local_landmarks is not None and local_image is not None:
            
            centerpoints = [11,12,23,24]
            # Get the average X and Y coordinates of the centerpoints
            x = 0
            y = 0
            for i in centerpoints:
                x += local_landmarks[i].x
                y += local_landmarks[i].y
            x /= len(centerpoints)
            y /= len(centerpoints)
            # print(x, y)
            # Get the quartile of the depth of the image, excluding 0s
            depth = local_image[local_image > 0]
            length = len(depth)
            if not length == 0:
                q10 = np.quantile(depth, 0.1)
                q90 = np.quantile(depth, 0.9)
                depth = depth[(depth >= q10) & (depth <= q90)]
                depth = np.mean(depth)/1000
                print(depth, length)
            else:
                depth = None
            if mode == "follow":
                joints[0] =0
                if depth is None:
                    x_vel = 0.0
                else:
                    x_vel = (depth-follow_dist)*1.0
                rot_vel = (x-0.5) * -2
                move.move(v_x=x_vel, v_y=0.0, v_rot=rot_vel)
            elif mode == "emote":
                joints[0] -= (x-0.5) * 0.35
                pass
            arm.moveJ(joints)
            local_landmarks = None
        rate.sleep()
        

    arm.arm_stow()
    print('Stowed.')
    rospy.sleep(1)
    move.sit()



if __name__ == '__main__':
    main()
