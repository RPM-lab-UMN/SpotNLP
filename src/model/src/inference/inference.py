import torch
import rospy
from model.model import GestureClassifier
from model.model_nn import GestureClassifierNN
from mp_pose.msg import buffer
import cv2
import numpy as np


def main():
    rospy.init_node('inference')
    class_pub = rospy.Publisher('/inference/class', rospy.String, queue_size=10)

    num_classes = 256
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Device: {device}')

    dataset_name = 'modalpha'
    mod_version = "NN"
    if mod_version == "PIO":
        model = GestureClassifier(num_classes=num_classes).to(device)
        batch_size = 64
    elif mod_version == "NN":
        model = GestureClassifierNN(num_classes=num_classes).to(device)
        batch_size = 256
    else:
        raise Exception("Invalid model version")
    model.eval()
    model.load_state_dict(torch.load(f'../{mod_version}_{dataset_name}.pth', map_location=torch.device('cpu')))
    model = model.to(device)

    frame_num = 0
    def model_callback(msg):
        nonlocal frame_num
        world_landmarks = np.array([np.array([np.array([keypoint.x, keypoint.y, keypoint.z, keypoint.visibility, keypoint.presence]) for keypoint in pose.world_landmarks]) for pose in msg.poses])
        world_landmarks = torch.from_numpy(world_landmarks).float().unsqueeze(0)
        world_landmarks = torch.flip(world_landmarks, [1])
        world_landmarks = world_landmarks.reshape(world_landmarks.shape[0], world_landmarks.shape[1], -1).to(device)
        output = model(world_landmarks, None).squeeze(1)
        output_val = torch.argmax(output, dim=1)[0].to('cpu')
        class_pub.publish(chr(output_val.item()))
        rospy.loginfo(f'Prediction: {chr(output_val.item())}')

        image = np.frombuffer(msg.color.data, dtype=np.uint8)
        image = image.reshape(msg.color.height, msg.color.width, -1)
        mask = np.frombuffer(msg.mask.data, dtype=np.uint8)
        mask = mask.reshape(msg.mask.height, msg.mask.width, -1)
        image = np.where(mask > 0, image, 0)
        cv2.addText(image, str(chr(output_val.item())), (20, 60), 'Arial', 48, (255, 0, 255), 2)
        cv2.addText(image, str(frame_num), (20, 120), 'Arial', 48, (255, 0, 255), 2)
        cv2.imshow('frame', image)
        cv2.waitKey(1)
        frame_num += 1


    message = None
    def message_callback(msg):
      nonlocal message
      message = msg

    rospy.Subscriber('/buffer/pose', buffer, message_callback)
    
    cv2.startWindowThread()
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('frame', np.zeros((100, 100, 3), dtype=np.uint8))

    while not rospy.is_shutdown():
      if message is not None:
        model_callback(message)
        message = None
      rospy.sleep(0.01)



        


if __name__ == '__main__':
    main()
