import rospy
import time
import math
import atexit
import numpy as np
from mp_pose.msg import people
from std_msgs.msg import Bool, Float32, String
from spotAPI import SpotAPI
from spotMove import SpotMove
from spotArm import SpotArm
from spotGraphNav import SpotGraphNav   

def main():
    rospy.init_node('SpotAPI')
    print("Launching SpotAPI")
    local_landmarks = None
    local_image = None
    # mode = False
    mode = {
        "state": "emote"
    }
    rospy.Subscriber('/movement/mode', String, lambda msg: mode.update({"state": msg.data}))
    follow_dist = 1.0
    def follow_dist_callback(msg):
        nonlocal follow_dist
        follow_dist = msg.data
    rospy.Subscriber('/movement/follow_distance', Float32, follow_dist_callback)

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
    graph = SpotGraphNav(spot)


    # arm.image_resolution('640x480')
    spot.power_on()
    # move.stand()
    # arm.arm_unstow()
    # print('Unstowed.')
    # sh0, sh1, el0, el1, wr0, wr1 = 0.0, -2.8, 1.5, -0.00, 1.35, 0.0
    # joints = [sh0, sh1, el0, el1, wr0, wr1]
    # arm.moveJ(joints)
    # arm.move_gripper(1.0)
    # spot.fan_power(0, 120)
    print('Moved arm.')
    rate = rospy.Rate(100)
    start_time = time.time()
    while not rospy.is_shutdown():
        if mode["state"] == "stand":
            if "deploy_arm" in mode:
                arm.arm_stow()
                mode.pop("deploy_arm")
            if "standing" not in mode:
                move.stand()
                mode["standing"] = True
        elif mode["state"] == "sit":
            if "deploy_arm" in mode:
                arm.arm_stow()
                mode.pop("deploy_arm")
            if "standing" in mode:
                move.sit()
                mode.pop("standing")
        elif mode["state"] == "graphnav":
            pass


        elif mode["state"] == "look" or mode["state"] == "follow":
            if "standing" not in mode:
                move.stand()
                mode["standing"] = True
            if "deploy_arm" not in mode:
                arm.arm_unstow()
                print('Unstowed.')
                sh0, sh1, el0, el1, wr0, wr1 = 0.0, -2.8, 1.5, -0.00, 1.35, 0.0
                joints = [sh0, sh1, el0, el1, wr0, wr1]
                arm.moveJ(joints)
                arm.move_gripper(1.0)
                mode["deploy_arm"] = True
            # Sin wave of seconds
            diff = time.time() - start_time
            light = (math.sin(diff*math.pi) + 1) / 2
            if mode["state"] == "follow":
                light = np.round(light)
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
                if mode["state"] == "follow":
                    joints[0] =0
                    if depth is None:
                        x_vel = 0.0
                    else:
                        x_vel = (depth-follow_dist)*1.0
                    rot_vel = (x-0.5) * -2
                    move.move(v_x=x_vel, v_y=0.0, v_rot=rot_vel)
                elif mode["state"] == "look":
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
