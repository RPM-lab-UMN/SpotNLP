from bosdyn.client.graph_nav import GraphNavClient
from bosdyn.client.map_processing import MapProcessingServiceClient
from bosdyn.client.recording import GraphNavRecordingServiceClient
from bosdyn.api.graph_nav import recording_pb2, map_pb2, nav_pb2, graph_nav_pb2
from BD.FrameHelpers import get_odom_tform_body
from bosdyn.client.exceptions import ResponseError
import json
import shutil
import os
import math
import rospy

class SpotGraphNav:
    def __init__(self, API, graph_folder=None, client_metadata=None):
        if client_metadata is None:
             client_metadata = GraphNavRecordingServiceClient.make_client_metadata(
                session_name='recording_test', 
                client_username=API._robot._current_user,  
                client_id='RecordingClient',
                client_type='Python SDK')
        self._robot = API._robot
        self._robot_state_client = API._robot_state_client
        self._command_client = API._command_client
        self._graph_nav_client = API._robot.ensure_client(GraphNavClient.default_service_name)
        self._recording_client = API._robot.ensure_client(GraphNavRecordingServiceClient.default_service_name)
        self._map_processing_client = API._robot.ensure_client(MapProcessingServiceClient.default_service_name)
        self._recording_environment = GraphNavRecordingServiceClient.make_recording_environment(
            waypoint_env=GraphNavRecordingServiceClient.make_waypoint_environment(
                client_metadata=client_metadata))
        
        self.graph_folder = graph_folder
        self.list_of_graphs = dict()
        self.waypoints = dict()
        self._current_graph = None
        self._current_graph_name = "None"
        self._current_edges = dict()  #maps to_waypoint to list(from_waypoint)
        self._current_waypoint_snapshots = dict()  # maps id to waypoint snapshot
        self._current_edge_snapshots = dict()  # maps id to edge snapshot
        self._current_annotation_name_to_wp_id = dict()
        self.update_list_of_graphs()
        self.stop_recording()
        self.clear_graph()

    def clear_graph(self):
        self._current_graph_name = "None"
        return self._graph_nav_client.clear_graph()
    
    def start_recording(self):
        self._current_graph_name = "Unsaved Graph"
        graph = self._graph_nav_client.download_graph()
        if graph is None:
            return (False, 'Failed to download graph')
        if (len(graph.waypoints) > 0):
            localization_state = self._graph_nav_client.get_localization_state()
            if not localization_state.localization.waypoint_id:
                return (False, 'Robot is not localized')
        try:
            self._recording_client.start_recording(recording_environment=self._recording_environment)
        except Exception as e:
            return (False, f'Failed to start recording: {e}')
        return (True, 'Recording started')
    
    def stop_recording(self):
        first_try = True
        while True:
            try:
                self._recording_client.stop_recording()
                break
            except Exception as e:
                if first_try:
                    first_try = False
                    continue
                return (False, f'Failed to stop recording: {e}')
        return (True, 'Recording stopped')
    
    def is_recording(self):
        return self._recording_client.get_record_status().is_recording
    
    def create_waypoint(self, waypoint_name, waypoint_description):
        response = self._recording_client.create_waypoint(waypoint_name=waypoint_name)
        # print(response)
        if response.status == recording_pb2.CreateWaypointResponse.STATUS_OK:
            x = response.created_waypoint.waypoint_tform_ko.position.x
            y = response.created_waypoint.waypoint_tform_ko.position.y
            z = response.created_waypoint.waypoint_tform_ko.position.z
            self.waypoints[waypoint_name] = {
                "description": waypoint_description, 
                "waypoint": {
                    "id": response.created_waypoint.id,
                    "snapshot_id": response.created_waypoint.snapshot_id,
                    "position": {"x": x, "y": y, "z": z,},
                },
                "created_edge": {
                    "id": {
                        "from_waypoint": response.created_edge.id.from_waypoint,
                        "to_waypoint": response.created_edge.id.to_waypoint,
                    },
                    "snapshot_id": response.created_edge.snapshot_id,
                },
            }
            return (True, response.created_waypoint.id)
        return (False, response.status)
    
    def download_full_graph(self, filepath, graph_information):
        self._current_graph_name = filepath
        self._current_graph = self._graph_nav_client.download_graph()
        if self._current_graph is None:
            return (False, 'Failed to download graph')
        filepath = os.path.join(self.graph_folder, filepath)
        if os.path.exists(filepath):
            shutil.rmtree(filepath)

        information_status = self.download_graph_information(filepath, graph_information)
        description_status = self.download_waypoint_descriptions(filepath)
        graph_status = self.download_graph(self._current_graph, filepath)
        waypoints_status = self.download_waypoints(self._current_graph.waypoints, filepath)
        edges_status = self.download_edges(self._current_graph.edges, filepath)
        self.update_list_of_graphs()
        return {
            'user_graph_description': information_status,
            'description': description_status,
            'graph': graph_status,
            'waypoints': waypoints_status,
            'edges': edges_status,
        }

    def download_graph_information(self, filepath, graph_information):
        os.makedirs(filepath, exist_ok=True)
        with open(os.path.join(filepath, 'graph_information.txt'), 'w') as f:
            f.write(graph_information)
        return (True, 'Graph information downloaded')


    def download_waypoint_descriptions(self, filepath):
        os.makedirs(filepath, exist_ok=True)
        with open(os.path.join(filepath, 'waypoint_descriptions.json'), 'w') as f:
            json.dump(self.waypoints, f, indent=4)  # Add indent parameter to make the JSON dump nicely formatted
        return (True, 'Waypoint descriptions downloaded')

    def download_graph(self, graph, filepath):
        status = self._write_bytes(filepath, 'graph', graph.SerializeToString())
        return (status, 'Graph downloaded')
        
    def download_waypoints(self, waypoints, filepath):
        output_message = ''
        num_waypoint_snapshots_downloaded = 0
        for waypoint in waypoints:
            if len(waypoint.snapshot_id) == 0:
                continue
            try:
                waypoint_snapshot = self._graph_nav_client.download_waypoint_snapshot(
                    waypoint.snapshot_id)
            except Exception:
                output_message += f'Failed to download waypoint snapshot: {waypoint.snapshot_id}\n'
                continue
            self._write_bytes(os.path.join(filepath, 'waypoint_snapshots'), str(waypoint.snapshot_id), waypoint_snapshot.SerializeToString())
            num_waypoint_snapshots_downloaded += 1
        output_message += f'Downloaded {num_waypoint_snapshots_downloaded} of the total {len(waypoints)} waypoint snapshots.\n'
        return (True, output_message)

    def download_edges(self, edges, filepath):
        output_message = ''
        num_edge_snapshots_downloaded = 0
        num_to_download = 0
        for edge in edges:
            if len(edge.snapshot_id) == 0:
                continue
            num_to_download += 1
            try:
                edge_snapshot = self._graph_nav_client.download_edge_snapshot(edge.snapshot_id)
            except Exception:
                output_message += f'Failed to download edge snapshot: {edge.snapshot_id}\n'
                continue
            self._write_bytes( os.path.join(filepath, 'edge_snapshots'), str(edge.snapshot_id), edge_snapshot.SerializeToString())
            num_edge_snapshots_downloaded += 1
        output_message += f'Downloaded {num_edge_snapshots_downloaded} of the total {num_to_download} edge snapshots.\n'
        return (True, output_message)
    
    def _write_bytes(self, filepath, filename, data):
        os.makedirs(filepath, exist_ok=True)
        with open(os.path.join(filepath, filename), 'wb+') as f:
            f.write(data)
            f.close()
        

    # TODO --------------------------------------------------------------
    def upload_full_graph(self, map_filepath):
        map_filepath = os.path.join(self.graph_folder, map_filepath)
        if not os.path.exists(map_filepath):
            return (False, 'The specified graph does not exist')
        
        with open(os.path.join(map_filepath + '/waypoint_descriptions.json'), 'r') as f:
            self.waypoints = json.load(f)


        with open(os.path.join(map_filepath + '/graph'), 'rb') as graph_file:
            # Load the graph from disk.
            data = graph_file.read()
            self._current_graph = map_pb2.Graph()
            self._current_graph.ParseFromString(data)
            print(f'Loaded graph has {len(self._current_graph.waypoints)} waypoints and {self._current_graph.edges} edges')
        for waypoint in self._current_graph.waypoints:
            # Load the waypoint snapshots from disk.
            with open(f'{map_filepath}/waypoint_snapshots/{waypoint.snapshot_id}','rb') as snapshot_file:
                waypoint_snapshot = map_pb2.WaypointSnapshot()
                waypoint_snapshot.ParseFromString(snapshot_file.read())
                self._current_waypoint_snapshots[waypoint_snapshot.id] = waypoint_snapshot
        for edge in self._current_graph.edges:
            if len(edge.snapshot_id) == 0:
                continue
            # Load the edge snapshots from disk.
            with open(f'{map_filepath}/edge_snapshots/{edge.snapshot_id}', 'rb') as snapshot_file:
                edge_snapshot = map_pb2.EdgeSnapshot()
                edge_snapshot.ParseFromString(snapshot_file.read())
                self._current_edge_snapshots[edge_snapshot.id] = edge_snapshot
        # Upload the graph to the robot.
        print('Uploading the graph and snapshots to the robot...')
        true_if_empty = not len(self._current_graph.anchoring.anchors)
        response = self._graph_nav_client.upload_graph(graph=self._current_graph,
                                                       generate_new_anchoring=true_if_empty)
        # Upload the snapshots to the robot.
        for snapshot_id in response.unknown_waypoint_snapshot_ids:
            waypoint_snapshot = self._current_waypoint_snapshots[snapshot_id]
            self._graph_nav_client.upload_waypoint_snapshot(waypoint_snapshot)
            print(f'Uploaded {waypoint_snapshot.id}')
        for snapshot_id in response.unknown_edge_snapshot_ids:
            edge_snapshot = self._current_edge_snapshots[snapshot_id]
            self._graph_nav_client.upload_edge_snapshot(edge_snapshot)
            print(f'Uploaded {edge_snapshot.id}')

        # The upload is complete! Check that the robot is localized to the graph,
        # and if it is not, prompt the user to localize the robot before attempting
        # any navigation commands.
        self._current_graph_name = map_filepath
        if not self.check_localization():
            return (False, 'The robot is not localized to the graph')

    def check_localization(self):
        localization_state = self._graph_nav_client.get_localization_state()
        if not localization_state.localization.waypoint_id:
            return False
        return True
    
    # def localize(self, waypoint_name):
    #     print(f"Localizing to {waypoint_name}")
    #     if waypoint_name not in self.waypoints:
    #         return (False, 'The specified waypoint does not exist')
    #     destination_waypoint = self.waypoints[waypoint_name]['waypoint']['id']

    #     robot_state = self._robot_state_client.get_robot_state()
    #     current_odom_tform_body = get_odom_tform_body(
    #         robot_state.kinematic_state.transforms_snapshot).to_proto()
    #     # Create an initial localization to the specified waypoint as the identity.
    #     localization = nav_pb2.Localization()
    #     localization.waypoint_id = destination_waypoint
    #     localization.waypoint_tform_body.rotation.w = 1.0
    #     self._graph_nav_client.set_localization(
    #         initial_guess_localization=localization,
    #         # It's hard to get the pose perfect, search +/-20 deg and +/-20cm (0.2m).
    #         max_distance=0.2,
    #         max_yaw=20.0 * math.pi / 180.0,
    #         fiducial_init=graph_nav_pb2.SetLocalizationRequest.FIDUCIAL_INIT_NO_FIDUCIAL,
    #         ko_tform_body=current_odom_tform_body)
    #     if not self.check_localization():
    #         return (False, 'Failed to localize the robot')
    #     return (True, 'Robot localized')
    
    def localize_to_waypoint(self, waypoint_name):
        print(f"Localizing to {waypoint_name}")
        if waypoint_name not in self.waypoints:
            print(self.waypoints)
            return (False, 'LOCAL: The specified waypoint does not exist')
        destination_waypoint = self.waypoints[waypoint_name]['waypoint']['id']
        robot_state = self._robot_state_client.get_robot_state()
        current_odom_tform_body = get_odom_tform_body(
            robot_state.kinematic_state.transforms_snapshot).to_proto()
        # Create an initial localization to the specified waypoint as the identity.
        localization = nav_pb2.Localization()
        localization.waypoint_id = destination_waypoint
        localization.waypoint_tform_body.rotation.w = 1.0
        self._graph_nav_client.set_localization(
            initial_guess_localization=localization,
            # It's hard to get the pose perfect, search +/-20 deg and +/-20cm (0.2m).
            max_distance=0.2,
            max_yaw=20.0 * math.pi / 180.0,
            fiducial_init=graph_nav_pb2.SetLocalizationRequest.FIDUCIAL_INIT_NO_FIDUCIAL,
            ko_tform_body=current_odom_tform_body)
        

    def go_to_waypoint(self, waypoint_name):
        if waypoint_name not in self.waypoints:
            print(self.waypoints)
            return (False, 'GOTO: The specified waypoint does not exist')
        destination_waypoint = self.waypoints[waypoint_name]['waypoint']['id']
        nav_to_cmd_id = None
        nav_to_cmd_id = self._graph_nav_client.navigate_to(destination_waypoint, 1.0, command_id=nav_to_cmd_id)
        
        is_finished = False
        while not is_finished:
            try:
                nav_to_cmd_id = self._graph_nav_client.navigate_to(destination_waypoint, 1.0, command_id=nav_to_cmd_id)
            except ResponseError as e:
                print(f'Error while navigating {e}')
                break
            rospy.sleep(.5)  
            is_finished = self._check_success(nav_to_cmd_id)
        return (True, f"Navigation to {waypoint_name} complete")
    
    def _check_success(self, command_id=-1):
        """Use a navigation command id to get feedback from the robot and sit when command succeeds."""
        if command_id == -1:
            # No command, so we have no status to check.
            return False
        status = self._graph_nav_client.navigation_feedback(command_id)
        if status.status == graph_nav_pb2.NavigationFeedbackResponse.STATUS_REACHED_GOAL:
            # Successfully completed the navigation commands!
            return True
        elif status.status == graph_nav_pb2.NavigationFeedbackResponse.STATUS_LOST:
            print('Robot got lost when navigating the route, the robot will now sit down.')
            return True
        elif status.status == graph_nav_pb2.NavigationFeedbackResponse.STATUS_STUCK:
            print('Robot got stuck when navigating the route, the robot will now sit down.')
            return True
        elif status.status == graph_nav_pb2.NavigationFeedbackResponse.STATUS_ROBOT_IMPAIRED:
            print('Robot is impaired.')
            return True
        else:
            # Navigation command is not complete yet.
            return False

    # END TODO ----------------------------------------------------------

    def update_list_of_graphs(self):
        self.list_of_graphs = dict()
        # Open the graph folder and list all the subfolders. One subfolder corresponds to one graph.
        for graph_name in os.listdir(self.graph_folder):
            graph_path = os.path.join(self.graph_folder, graph_name)
            # Get the number of waypoints from 'waypoint_descriptions.json'
            try:
                with open(os.path.join(graph_path, 'waypoint_descriptions.json'), 'r') as f:
                    waypoint_descriptions = json.load(f)
                    waypoints = list(waypoint_descriptions.keys())
                    num_waypoints = len(waypoints)
            except FileNotFoundError:
                waypoints = []
                num_waypoints = 0

            # Get the graph information from 'graph_information.txt'
            try:
                with open(os.path.join(graph_path, 'graph_information.txt'), 'r') as f:
                    graph_information = f.read()
            except FileNotFoundError:
                graph_information = 'No information available.'

            self.list_of_graphs[graph_name] = {
                'name': graph_name,
                'graph_information': graph_information,
                'num_waypoints': num_waypoints,
                'waypoints': waypoints,
            }


    def get_status(self):
        return {
            'current_graph': {
                'name': self._current_graph_name,
                'recording': self.is_recording(),
                'num_waypoints': len(self.waypoints),
                'waypoints': self.waypoints,
                'localization': self.check_localization(),
            },
            'stored_graphs': {
                'num_graphs': len(self.list_of_graphs),
                'graphs': self.list_of_graphs,
            },
        }