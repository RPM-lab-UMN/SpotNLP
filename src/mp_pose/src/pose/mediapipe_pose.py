# mamba activate burn
import mediapipe as mp
import cv2 
import numpy as np
import rospy
from mp_pose.msg import people, person, pose, landmark, depth_image
from sensor_msgs.msg import Image
import rospkg


def parse_result(result, output_image, header):
    msg = people()
    msg.header = header
    msg.num_people = len(result.pose_landmarks)

    for i in range(msg.num_people):
        # Generate person message
        person_msg = person()
        person_msg.pose = pose()
        person_msg.pose.header = header
        person_msg.pose.local_landmarks = []
        person_msg.pose.world_landmarks = []

        # Add landmarks to person message
        for landmark_point in result.pose_landmarks[i]:
            point = landmark()
            point.x = landmark_point.x
            point.y = landmark_point.y
            point.z = landmark_point.z
            point.visibility = landmark_point.visibility
            point.presence = landmark_point.presence
            person_msg.pose.local_landmarks.append(point)
        for landmark_point in result.pose_world_landmarks[i]:
            point = landmark()
            point.x = landmark_point.x
            point.y = landmark_point.y
            point.z = landmark_point.z
            point.visibility = landmark_point.visibility
            point.presence = landmark_point.presence
            person_msg.pose.world_landmarks.append(point)

        # Generate segmentation mask
        seg_mask =  np.array(result.segmentation_masks[i].numpy_view(), dtype=np.float32)
        seg_mask = np.where(seg_mask > 0.5, 255, 0)
        person_image = np.array(seg_mask, dtype=np.uint8)
        
        # Convert to sensor_msgs/Image
        person_msg.image = Image()
        person_msg.image.height, person_msg.image.width = person_image.shape[:2]
        person_msg.image.data = person_image.tobytes()
        person_msg.image.encoding = "mono8"
        person_msg.image.header = header
        
        # Add person to people message
        msg.people.append(person_msg)
    return msg

def main():
    rospy.init_node('mediapipe_pose', anonymous=True)
    pub = rospy.Publisher('/pose/people', people, queue_size=10)

    BaseOptions = mp.tasks.BaseOptions
    PoseLandmarker = mp.tasks.vision.PoseLandmarker
    PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    path = rospkg.RosPack().get_path('mp_pose')
    base_options = BaseOptions(
        model_asset_path=path + '/src/pose/pose_landmarker_heavy.task')
    options = PoseLandmarkerOptions(
        base_options=base_options, 
        running_mode=VisionRunningMode.VIDEO,
        num_poses=4,
        # result_callback=print_result,
        output_segmentation_masks=True)
    detector = PoseLandmarker.create_from_options(options)

    print("Ready to detect pose... \n\n")

    with PoseLandmarker.create_from_options(options) as landmarker:
        def image_callback(msg):
            mp_image = np.frombuffer(msg.color.data, dtype=np.uint8)
            mp_image = mp_image.reshape(msg.color.height, msg.color.width, -1)
            mp_image = cv2.cvtColor(mp_image, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=mp_image)
            frame_timestamp_ms = int(msg.header.stamp.to_nsec() / 1000000)
            result = landmarker.detect_for_video(mp_image, frame_timestamp_ms)
            out_msg = parse_result(result, mp_image, msg.header)
            out_msg.color = msg.color
            out_msg.depth = msg.depth
            pub.publish(out_msg)
            
        rospy.Subscriber('/pose/rgbd_image', depth_image, image_callback)
        rospy.spin()


if __name__ == '__main__':
    print("Do you have a moment to talk about our lord and savior, Jebbus?")
    main()