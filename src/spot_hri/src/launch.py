import rospy
import rospkg
import rosgraph
import roslib
import subprocess
import os
import atexit
import os
import signal

def cleanup_processes(processes):
    for process in processes:
        if process is not None:
            os.kill(process.pid, signal.SIGINT)
    print("Killed all processes")


def launch_node(params, log_dir):
    name, package, script = params['name'], params['package'], params['script']
    if name == 'Sleep':
        rospy.loginfo(f"Sleeping for {package} seconds")
        rospy.sleep(package)
        return None
    script_path = roslib.packages.get_pkg_dir(package) + '/' + script
    log_file = open(os.path.join(log_dir, f"{name}.log"), "w")
    process = subprocess.Popen(['python3', '-u', script_path], stdout=log_file, stderr=subprocess.STDOUT)
    rospy.loginfo(f"Launched node: {name}")
    return process

def start_roscore():
    process = subprocess.Popen(['roscore'])
    rospy.loginfo(f"Launched node: roscore")
    return process

def main():
    processes = []
    atexit.register(cleanup_processes, processes)

    if not rosgraph.is_master_online():
        processes.append(start_roscore())
    rospy.init_node('launch_nodes')

    log_dir = rospkg.RosPack().get_path('spot_hri') + '/log'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    spot = True
    if spot:
        camera = {'name': 'Spot Camera', 'package': 'camera', 'script': 'src/spot_hand/hand_rgbd.py'}
    else:
        camera = {'name': 'RealSense Camera', 'package': 'camera', 'script': 'src/realsense/realsense.py'}

    nodes = [
        {'name': 'Movement', 'package': 'movement_core', 'script': 'src/spot/spot.py'},
        {'name': 'Sleep', 'package': 5, 'script': 'sleep'},
        {'name': 'MediaPipe', 'package': 'mp_pose', 'script': 'src/pose/mediapipe_pose.py'},
        {'name': 'Xmem', 'package': 'xmem', 'script': 'src/XMem/xmem.py'},
        # {'name': 'Buffer', 'package': 'gesture', 'script': 'src/buffer/people_buffer.py'},
        # {'name': 'Inference', 'package': 'model', 'script': 'src/inference/inference.py'},
        # {'name': 'Event', 'package': 'state_core', 'script': '/src/event/event.py'},
        # {'name': 'SM', 'package': 'state_core', 'script': '/src/state_machine/sm.py'},
        # {'name': 'TTS', 'package': 'tts', 'script': 'src/tts/speech.py'},
        camera,
    ]

    for node in nodes:
        processes.append(launch_node(node, log_dir))

    rospy.spin()


if __name__ == '__main__':
    main()
