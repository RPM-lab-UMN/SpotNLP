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

    def power_off(self):
        self._robot.power_off(cut_immediately=False)
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


    def get_status(self):
        status = self._robot_state_client.get_robot_state()
        # print(status)
        motor_states = {
            0: 'MOTOR_POWER_STATE_UNKNOWN',
            1: 'MOTOR_POWER_STATE_OFF',
            2: 'MOTOR_POWER_STATE_ON',
            3: 'MOTOR_POWER_STATE_POWERING_ON',
            4: 'MOTOR_POWER_STATE_POWERING_OFF',
            5: 'MOTOR_POWER_STATE_ERROR',
        }
        shore_power_states = {
            0: 'SHORE_POWER_STATE_UNKNOWN',
            1: 'SHORE_POWER_STATE_ON',
            2: 'SHORE_POWER_STATE_OFF',
        }
        battery_states = {
            0: 'STATUS_UNKNOWN',
            1: 'STATUS_MISSING',
            2: 'STATUS_CHARGING',
            3: 'STATUS_DISCHARGING',
            4: 'STATUS_BOOTING',
        }
        stow_states = {
            0: 'STOWSTATE_UNKNOWN',
            1: 'STOWSTATE_STOWED',
            2: 'STOWSTATE_DEPLOYED',    
        }
        carry_states = {
            0: 'CARRY_STATE_UNKNOWN',
            1: 'CARRY_STATE_NOT_CARRIABLE',
            2: 'CARRY_STATE_CARRIABLE',
            3: 'CARRY_STATE_CARRIABLE_AND_STOWABLE',
        }
        estop_states = {
            0: 'STATE_UNKNOWN',
            1: 'STATE_ESTOPPED',
            2: 'STATE_NOT_ESTOPPED',
        }
        estops = {}
        for estop in status.estop_states:
            estops[estop.name] = estop_states[estop.state]
        
        return {
            "motor_power_state": motor_states[status.power_state.motor_power_state],
            "shore_power_state": shore_power_states[status.power_state.shore_power_state],
            "battery_states": {
                "charge_percentage": status.battery_states[0].charge_percentage.value,
                "estimated_runtime": status.battery_states[0].estimated_runtime.seconds,
                "status": battery_states[status.battery_states[0].status],
                "voltage": status.battery_states[0].voltage.value,
                "current": status.battery_states[0].current.value,
            },
            "manipulator_state": {
                "stow_state": stow_states[status.manipulator_state.stow_state],
                "gripper_open_percentage": status.manipulator_state.gripper_open_percentage,
                "carry_state": carry_states[status.manipulator_state.carry_state],
            },
            "estop_status": estops,
            # "position": {} # TODO: Add position
        }




