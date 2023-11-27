import torch
import rospy
from mp_pose.msg import people, pose, landmark
import torch
import numpy as np
from PIL import Image
from model.network import XMem
from inference.inference_core import InferenceCore
import cv2
from inference.interact.interactive_utils import image_to_torch, index_numpy_to_one_hot_torch, torch_prob_to_numpy_mask, overlay_davis

def check_init_pose(pose):
  # Check if pose is a T pose
  landmarks = pose.local_landmarks
  # 16: Right Wrist; 15: Left Wrist 
  # 14: Right Elbow; 13: Left Elbow 
  # 12: Right Shoulder; 11: Left Shoulder
  # This is a T pose all joints are in a straight line
  points = [16, 15, 14, 13, 12, 11]
  head = [0]
  for point in points+head:
    if landmarks[point].visibility < 0.5:
      return False
  y_heights = []
  for point in points:
    y_heights.append(landmarks[point].y)
  y_heights = np.array(y_heights)
  # Check if all y heights are within 0.1 of each other
  if np.max(y_heights) - np.min(y_heights) > 0.1:
    print(np.max(y_heights), np.min(y_heights))
    return False
  return True

def main():
  rospy.init_node('xmem', anonymous=True)
  pub_people = rospy.Publisher('/xmem/people', people, queue_size=10)
  pub_pose = rospy.Publisher('/xmem/pose', pose, queue_size=10)
  torch.set_grad_enabled(False)
  torch.cuda.empty_cache()
  if torch.cuda.is_available():
    print('Using GPU')
    device = 'cuda'
  else:
    print('CUDA not available. Please connect to a GPU instance if possible.')
    device = 'cpu'
    
  config = {
      'top_k': 30,
      'mem_every': 5,
      'deep_update_every': -1,
      'enable_long_term': True,
      'enable_long_term_count_usage': True,
      'num_prototypes': 128,
      'min_mid_term_frames': 5,
      'max_mid_term_frames': 10,
      'max_long_term_elements': 10000,
      # 'single_object': True,
  }
  network = XMem(config, './saves/XMem.pth').eval().to(device)

  num_objects = 1
  processor = InferenceCore(network, config=config)
  processor.set_all_labels(range(1, num_objects+1)) # consecutive labels

  init_mask = None
  with torch.cuda.amp.autocast(enabled=True):
    def people_callback(msg):
      nonlocal init_mask
      nonlocal processor
      nonlocal device
      nonlocal num_objects

      frame = np.frombuffer(msg.color.data, dtype=np.uint8)
      frame = frame.reshape(msg.color.height, msg.color.width, -1)
      frame_torch, _ = image_to_torch(np.copy(frame), device=device)
      if init_mask is None:
        #TODO Check if any pose is a T pose
        for i in range(msg.num_people):
          valid = check_init_pose(msg.people[i].pose)
          if valid:
            mask = np.frombuffer(msg.people[i].image.data, dtype=np.uint8)
            mask = mask.reshape(msg.people[i].image.height, msg.people[i].image.width, -1)
            # Convert 255 to 1
            mask = np.where(mask > 0, 1, 0)
            mask = mask[:,:,0]
            mask_torch = index_numpy_to_one_hot_torch(mask, num_objects+1).to(device)
            prediction = processor.step(frame_torch, mask_torch[1:])
            init_mask = True
            print('Initialized')
        return
      prediction = processor.step(frame_torch)
      # prediction = torch_prob_to_numpy_mask(prediction)
      # Visualize
      prediction = prediction.to('cpu').detach().numpy()
      
      max_IOU = 0.92
      person_out = None
      for i in range(msg.num_people):
        mask = np.frombuffer(msg.people[i].image.data, dtype=np.uint8)
        mask = mask.reshape(msg.people[i].image.height, msg.people[i].image.width, -1)
        mask = np.where(mask > 0, 1, 0)
        mask = mask[:,:,0]
        mask = mask.astype(np.uint8)
        # Calculate IoU
        pred = np.where(prediction[1] > 0.5, 1, 0)
        intersection = np.logical_and(pred, mask)
        union = np.logical_or(pred, mask) + 1e-6
        iou_score = np.sum(intersection) / np.sum(union)
        print('IoU score: ', iou_score)
        if iou_score > max_IOU:
          max_IOU = iou_score
          person_out = msg.people[i]
      if person_out is not None:
        msg.num_people = 1
        msg.people = [person_out]
        pub_people.publish(msg)
        pub_pose.publish(person_out.pose)

      cv2.imshow('frame', prediction[1])
      cv2.waitKey(1)
      del prediction
      del frame_torch
      torch.cuda.empty_cache()

    people_message = None
    def message_callback(msg):
      nonlocal people_message
      people_message = msg

    rospy.Subscriber('/pose/people', people, message_callback)
    
    while not rospy.is_shutdown():
      if people_message is not None:
        people_callback(people_message)
        people_message = None
      rospy.sleep(0.01)
    
if __name__ == '__main__':
  main()