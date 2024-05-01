from bosdyn.client.robot_command import RobotCommandBuilder, block_until_arm_arrives
from bosdyn.client.frame_helpers import GRAV_ALIGNED_BODY_FRAME_NAME, ODOM_FRAME_NAME, get_a_tform_b
from bosdyn.api import geometry_pb2, arm_command_pb2, synchronized_command_pb2, robot_command_pb2
from bosdyn.api import gripper_camera_param_pb2
from google.protobuf import wrappers_pb2
from bosdyn.client import math_helpers


class SpotArm:
    def __init__(self, API):
        self._robot = API._robot
        self._command_client = API._command_client
        self._robot_state_client = API._robot_state_client
        self._gripper_param_client = API._gripper_param_client
        
    def arm_unstow(self):
        unstow = RobotCommandBuilder.arm_ready_command()
        unstow_command_id = self._command_client.robot_command(unstow)
        self._command_client.robot_command_feedback(unstow_command_id)
        print('Unstowing arm...')
        block_until_arm_arrives(self._command_client, unstow_command_id, 3.0)

    def arm_stow(self, gripper=None):
        if gripper is not None:
            self.move_gripper(gripper)
            self.gripper_light(False, 0.0)
        stow = RobotCommandBuilder.arm_stow_command()
        stow_command_id = self._command_client.robot_command(stow)
        self._command_client.robot_command_feedback(stow_command_id)
        print('Stowing arm...')
        block_until_arm_arrives(self._command_client, stow_command_id, 3.0)

    def move_gripper(self, fraction):
        open_gripper = RobotCommandBuilder.claw_gripper_open_fraction_command(fraction)
        open_gripper_command_id = self._command_client.robot_command(open_gripper)
        self._command_client.robot_command_feedback(open_gripper_command_id)
        print(f'Opening gripper {fraction}...')

    def light_on(self):
        light_on = RobotCommandBuilder.led_command(1, 1, 1)
        light_on_command_id = self._command_client.robot_command(light_on)
        self._command_client.robot_command_feedback(light_on_command_id)
        print('Turning light on...')

        
    def moveL(self, x, y, z, qx, qy, qz, qw):
        hand_ewrt_flat_body = geometry_pb2.Vec3(x=x, y=y, z=z)
        flat_body_Q_hand = geometry_pb2.Quaternion(w=qw, x=qx, y=qy, z=qz)
        flat_body_T_hand = geometry_pb2.SE3Pose(position=hand_ewrt_flat_body,
                                                rotation=flat_body_Q_hand)

        robot_state = self._robot_state_client.get_robot_state()
        odom_T_flat_body = get_a_tform_b(robot_state.kinematic_state.transforms_snapshot,
                                         ODOM_FRAME_NAME, GRAV_ALIGNED_BODY_FRAME_NAME)
        odom_T_hand = odom_T_flat_body * math_helpers.SE3Pose.from_proto(flat_body_T_hand)
        seconds = 2

        arm_command = RobotCommandBuilder.arm_pose_command(
            odom_T_hand.x, odom_T_hand.y, odom_T_hand.z, odom_T_hand.rot.w, odom_T_hand.rot.x,
            odom_T_hand.rot.y, odom_T_hand.rot.z, ODOM_FRAME_NAME, seconds)
        
        arm_command_id = self._command_client.robot_command(arm_command)
        self._command_client.robot_command_feedback(arm_command_id)
        block_until_arm_arrives(self._command_client, arm_command_id, seconds)
        print(f'Moving arm to {x}, {y}, {z}, {qx}, {qy}, {qz}, {qw}...')


    def _make_robot_command(self, arm_joint_traj):
        """ Helper function to create a RobotCommand from an ArmJointTrajectory.
            The returned command will be a SynchronizedCommand with an ArmJointMoveCommand
            filled out to follow the passed in trajectory. """

        joint_move_command = arm_command_pb2.ArmJointMoveCommand.Request(trajectory=arm_joint_traj)
        arm_command = arm_command_pb2.ArmCommand.Request(arm_joint_move_command=joint_move_command)
        sync_arm = synchronized_command_pb2.SynchronizedCommand.Request(arm_command=arm_command)
        arm_sync_robot_cmd = robot_command_pb2.RobotCommand(synchronized_command=sync_arm)
        return RobotCommandBuilder.build_synchro_command(arm_sync_robot_cmd)

    def moveJ(self, joints, block=False):
        sh0, sh1, el0, el1, wr0, wr1 = joints
        traj_point = RobotCommandBuilder.create_arm_joint_trajectory_point(
            sh0, sh1, el0, el1, wr0, wr1)
        max_vel = wrappers_pb2.DoubleValue(value=5)
        max_acc = wrappers_pb2.DoubleValue(value=1)
        arm_joint_traj = arm_command_pb2.ArmJointTrajectory(
            points=[traj_point], maximum_velocity=max_vel, maximum_acceleration=max_acc)
        command = self._make_robot_command(arm_joint_traj)
        cmd_id = self._command_client.robot_command(command)
        if block:
            self._command_client.robot_command_feedback(cmd_id)
            block_until_arm_arrives(self._command_client, cmd_id, 5.0)

    # def velocityJ(self, joints, block=False):
    #     sh0, sh1, el0, el1, wr0, wr1 = joints
    #     traj_point = RobotCommandBuilder.


    def gripper_light(self, LED_on, fraction):
        # params = gripper_camera_param_pb2.GripperCameraParams(
        # camera_mode=camera_mode, brightness=brightness, contrast=contrast, gain=gain,
        # saturation=saturation, focus_absolute=manual_focus, focus_auto=auto_focus,
        # exposure_absolute=exposure, exposure_auto=auto_exposure, hdr=hdr, led_mode=led_mode,
        # led_torch_brightness=led_torch_brightness, gamma=gamma, sharpness=sharpness,
        # white_balance_temperature=white_balance_temperature,
        # white_balance_temperature_auto=white_balance_temperature_auto)

        if LED_on:
            led_mode = gripper_camera_param_pb2.GripperCameraParams.LED_MODE_TORCH
            led_torch_brightness = wrappers_pb2.FloatValue(value=fraction)
        else:
            led_mode = gripper_camera_param_pb2.GripperCameraParams.LED_MODE_OFF
            led_torch_brightness = None
        # camera_mode = gripper_camera_param_pb2.GripperCameraParams.MODE_4208_3120
        params = gripper_camera_param_pb2.GripperCameraParams(
            led_mode=led_mode, led_torch_brightness=led_torch_brightness)

        request = gripper_camera_param_pb2.GripperCameraParamRequest(params=params)
        response = self._gripper_param_client.set_camera_params(request)

    def image_resolution(self, resolution):
        camera_mode = None
        if resolution is not None:
            if resolution == '640x480':
                camera_mode = gripper_camera_param_pb2.GripperCameraParams.MODE_640_480
            elif resolution == '1280x720':
                camera_mode = gripper_camera_param_pb2.GripperCameraParams.MODE_1280_720
            elif resolution == '1920x1080':
                camera_mode = gripper_camera_param_pb2.GripperCameraParams.MODE_1920_1080
            elif resolution == '3840x2160':
                camera_mode = gripper_camera_param_pb2.GripperCameraParams.MODE_3840_2160
            elif resolution == '4096x2160':
                camera_mode = gripper_camera_param_pb2.GripperCameraParams.MODE_4096_2160
            elif resolution == '4208x3120':
                camera_mode = gripper_camera_param_pb2.GripperCameraParams.MODE_4208_3120

        request = gripper_camera_param_pb2.GripperCameraParamRequest(
            params=gripper_camera_param_pb2.GripperCameraParams(camera_mode=camera_mode))
        response = self._gripper_param_client.set_camera_params(request)
