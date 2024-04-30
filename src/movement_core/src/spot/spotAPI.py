import os
import bosdyn.client
import bosdyn.client.util
from bosdyn.client.robot_command import RobotCommandClient
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.power import PowerClient
from bosdyn.client.gripper_camera_param import GripperCameraParamClient

class SpotAPI:    
    def __init__(self, robot_ip='BOSDYN_W_IP'):
        self._sdk = bosdyn.client.create_standard_sdk('spot-python')
        self._robot = self._sdk.create_robot(os.environ[robot_ip])
        self._id_client = self._robot.ensure_client('robot-id')
        response = self._id_client.get_id_async().result()
        print(f'Connected to {response.nickname}...')
        # print(response)
        self._robot.authenticate(os.environ['BOSDYN_CLIENT_USERNAME'], 
                                 os.environ['BOSDYN_CLIENT_PASSWORD'])
        print('Authenticated...')
        self._lease_client = self._robot.ensure_client('lease')
        self._lease = self._lease_client.acquire()
        self._lease_keep_alive = bosdyn.client.lease.LeaseKeepAlive(self._lease_client)
        print(f'Lease status: {self._lease_keep_alive.is_alive()}')
        self._robot.time_sync.wait_for_sync()
        self._command_client = self._robot.ensure_client(RobotCommandClient.default_service_name)
        self._robot_state_client = self._robot.ensure_client(RobotStateClient.default_service_name)
        self._power_client = self._robot.ensure_client(PowerClient.default_service_name)
        self._gripper_param_client = self._robot.ensure_client(GripperCameraParamClient.default_service_name)


    def estop_start(self):
        self._estop_client = self._robot.ensure_client('estop')
        self._estop_endpoint = bosdyn.client.estop.EstopEndpoint(
            client=self._estop_client, name='eStop', estop_timeout=9.0)
        self._estop_endpoint.force_simple_setup()
        self._estop_keep_alive = bosdyn.client.estop.EstopKeepAlive(self._estop_endpoint)
        print(f'eStop status: {self._estop_client.get_status().stop_level}')

    def __del__(self):
        if self._robot.is_powered_on():
            self._robot.power_off(cut_immediately=False)
        if hasattr(self, '_lease_keep_alive'):
            self._lease_client.return_lease(self._lease)
            self._lease_keep_alive.shutdown()
        if hasattr(self, '_estop_keep_alive'):
            self._estop_keep_alive.shutdown()

    def power_on(self):
        self._robot.power_on(timeout_sec=20)
        print(f'Robot is powered on: {self._robot.is_powered_on()}')

    def fan_power(self,power, duration): 
        self._power_client.fan_power_command_async(percent_power=power, duration=duration)

    def __del__(self):
        if self._robot.is_powered_on():
            self._robot.power_off(cut_immediately=False)
        if hasattr(self, '_lease_keep_alive'):
            self._lease_client.return_lease(self._lease)
            self._lease_keep_alive.shutdown()
        if hasattr(self, '_estop_keep_alive'):
            self._estop_keep_alive.shutdown()
        print('SpotAPI deleted...')





