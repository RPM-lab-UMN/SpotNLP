import rospy
import argparse
import rosbag
import rospy
import cv2
import numpy as np
import colorsys
import rospkg
# from gesture import Dataset
# print contents of gesture
# import gesture
import gesture
print(dir(gesture))
print(gesture.__file__)
print(gesture.__path__)
print(gesture.__package__)
print(gesture.__name__)

exit()

def keypoints_on_image(keypoints, image, dot_color):
    for keypoint in keypoints:
        x = int(keypoint.x * image.shape[1])
        y = int(keypoint.y * image.shape[0])
        cv2.circle(image, (x, y), 5, dot_color, -1)
    return image

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_name', nargs='?', default='data', help='Name of the data to save')
    args = parser.parse_args()

    rospy.init_node('pose_buffer', anonymous=True)
    path = rospkg.RosPack().get_path('gesture') + f'/data/{args.data_name}.bag'
    bag = rosbag.Bag(path, 'r')

    msg_num = 0
    data = list(bag.read_messages(topics=['/buffer/pose']))
    while msg_num < len(data):
        topic, msg, t = data[msg_num]
        image = np.frombuffer(msg.color.data, dtype=np.uint8)
        image = image.reshape(msg.color.height, msg.color.width, -1)
        mask = np.frombuffer(msg.mask.data, dtype=np.uint8)
        mask = mask.reshape(msg.mask.height, msg.mask.width, -1)
        image = np.where(mask > 0, image, 0)

        num = 10
        amount = num if len(msg.poses) > num else len(msg.poses)
        offset = len(msg.poses) - amount
        for i in range(amount):
            # Color: Start at blue and go to red
            # dot_color = (int(255 * (i/amount)), int(255 * (i/amount)), int(255 * (1 - i/amount)))
            # Use HSV to rotate through colors
            hue = int(360 * (i / amount))
            hsv_color = colorsys.hsv_to_rgb(hue / 360, 1, 1)
            dot_color = tuple(int(255 * c) for c in hsv_color)
            image = keypoints_on_image(msg.poses[offset+i].local_landmarks, image, dot_color)

        # image = cv2.resize(image, (image.shape[1]*3, image.shape[0]*3))
        # Show maximized
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        cv2.imshow('frame', image)
        gt = cv2.waitKey(0)
        if gt == 190:
            print('Exiting')
            break
        elif gt == 255:
            print(f'Redoing message {msg_num-1}')
            msg_num -= 1
            # TODO: pop from data
        else:
            print(f'GT: {gt}, Frame: {msg_num}, Length: {len(msg.poses)}')
            # TODO: save to file
            msg_num += 1

    bag.close()

if __name__ == '__main__':
    main()
