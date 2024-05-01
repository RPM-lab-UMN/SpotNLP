from bosdyn.client.exceptions import ResponseError, RpcError
from bosdyn.client.lease import Error as LeaseBaseError
from bosdyn.client.robot_command import RobotCommandBuilder, blocking_stand, blocking_sit
import time

class SpotMove:
    def __init__(self, API, duration_sec=0.5):
        self._robot = API._robot
        self._command_client = API._command_client
        self.duration_sec = duration_sec

    def stand(self):
        cmd = RobotCommandBuilder.synchro_stand_command()
        self._command_client.robot_command(cmd)
        print('Standing...')
        blocking_stand(self._command_client, timeout_sec=10)

    def sit(self):
        cmd = RobotCommandBuilder.synchro_sit_command()
        self._command_client.robot_command(cmd)
        print('Sitting...')
        blocking_sit(self._command_client, timeout_sec=10)

    
    def _velocity_cmd_helper(self, desc='', v_x=0.0, v_y=0.0, v_rot=0.0):
        self._start_robot_command(
            desc, RobotCommandBuilder.synchro_velocity_command(v_x=v_x, v_y=v_y, v_rot=v_rot),
            end_time_secs=time.time() + self.duration_sec)
        
    def move(self, v_x=0.0, v_y=0.0, v_rot=0.0):
        # print(f'Moving: v_x={v_x}, v_y={v_y}, v_rot={v_rot}', end='\r')
        self._velocity_cmd_helper('Moving...', v_x=v_x, v_y=v_y, v_rot=v_rot)


    def _try_grpc(self, desc, thunk):
        try:
            return thunk()
        except (ResponseError, RpcError, LeaseBaseError) as err:
            print(f'Failed {desc}: {err}')
            return None
        
    def _start_robot_command(self, desc, command_proto, end_time_secs=None):
        def _start_command():
            self._command_client.robot_command(command=command_proto,
                                                     end_time_secs=end_time_secs)
        self._try_grpc(desc, _start_command)

