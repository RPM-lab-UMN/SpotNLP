from bosdyn.client.graph_nav import GraphNavClient
from bosdyn.client.map_processing import MapProcessingServiceClient
from bosdyn.client.recording import GraphNavRecordingServiceClient
from bosdyn.api.graph_nav import recording_pb2
import os

class SpotGraphNav:
    def __init__(self, API, client_metadata=None):
        if client_metadata is None:
             client_metadata = GraphNavRecordingServiceClient.make_client_metadata(
                session_name='recording_test', 
                client_username=API._robot._current_user,  
                client_id='RecordingClient',
                client_type='Python SDK')
        self._robot = API._robot
        self._command_client = API._command_client
        self._graph_nav_client = API._robot.ensure_client(GraphNavClient.default_service_name)
        self._recording_client = API._robot.ensure_client(GraphNavRecordingServiceClient.default_service_name)
        self._map_processing_client = API._robot.ensure_client(MapProcessingServiceClient.default_service_name)
        self._recording_environment = GraphNavRecordingServiceClient.make_recording_environment(
            waypoint_env=GraphNavRecordingServiceClient.make_waypoint_environment(
                client_metadata=client_metadata))
        
        self.graph_folder = "./graph" # TODO: Change this to the correct path

        self._current_graph = None
        self._current_edges = dict()  #maps to_waypoint to list(from_waypoint)
        self._current_waypoint_snapshots = dict()  # maps id to waypoint snapshot
        self._current_edge_snapshots = dict()  # maps id to edge snapshot
        self._current_annotation_name_to_wp_id = dict()

    def clear_graph(self):
        return self._graph_nav_client.clear_graph()
    
    def start_recording(self):
        graph = self._graph_nav_client.download_graph()
        if graph is None:
            return (False, 'Failed to download graph')
        if (len(graph.waypoints) > 0):
            localization_state = self._graph_nav_client.get_localization_state()
            if not localization_state.localization.waypoint_id:
                return (False, 'Robot is not localized')
        try:
            self._recording_client.start_recording(self._recording_environment)
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
        return self._recording_client.is_recording()
    
    def create_waypoint(self, waypoint_name):
        response = self._graph_nav_client.create_waypoint(waypoint_name)
        if response.status == recording_pb2.CreateWaypointResponse.STATUS_OK:
            return (True, response.waypoint_id)
        return (False, response.status)
    
    def _write_to_file(self, filepath, filename, data):
        os.makedirs(filepath, exist_ok=True)
        with open(filename, 'wb') as f:
            f.write(data)
            f.close()

    def download_full_graph(self):
        graph = self._graph_nav_client.download_graph()
        if graph is None:
            return (False, 'Failed to download graph')
        graph_status = self.download_graph(graph)
        waypoints_status = self.download_waypoints(graph.waypoints)
        edges_status = self.download_edges(graph.edges)
        return {
            'graph': graph_status,
            'waypoints': waypoints_status,
            'edges': edges_status,
        }

    def download_graph(self, graph):
        status = self._write_to_file(self.graph_folder, 'graph', graph.SerializeToString())
        return (status, 'Graph downloaded')

        
    def download_waypoints(self, waypoints):
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
            self._write_bytes(os.path.join(self._download_filepath, 'waypoint_snapshots'),
                              str(waypoint.snapshot_id), waypoint_snapshot.SerializeToString())
            num_waypoint_snapshots_downloaded += 1
        output_message += f'Downloaded {num_waypoint_snapshots_downloaded} of the total {len(waypoints)} waypoint snapshots.\n'
        return (True, output_message)

    def download_edges(self, edges):
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
            self._write_bytes(os.path.join(self._download_filepath, 'edge_snapshots'),
                              str(edge.snapshot_id), edge_snapshot.SerializeToString())
            num_edge_snapshots_downloaded += 1
        output_message += f'Downloaded {num_edge_snapshots_downloaded} of the total {num_to_download} edge snapshots.\n'
        return (True, output_message)
        
        
    def upload_graph(self):
        pass
        
    

    


        

        
    




