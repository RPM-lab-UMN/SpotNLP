;; Auto-generated. Do not edit!


(when (boundp 'mp_pose::pose_image)
  (if (not (find-package "MP_POSE"))
    (make-package "MP_POSE"))
  (shadow 'pose_image (find-package "MP_POSE")))
(unless (find-package "MP_POSE::POSE_IMAGE")
  (make-package "MP_POSE::POSE_IMAGE"))

(in-package "ROS")
;;//! \htmlinclude pose_image.msg.html
(if (not (find-package "SENSOR_MSGS"))
  (ros::roseus-add-msgs "sensor_msgs"))
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass mp_pose::pose_image
  :super ros::object
  :slots (_header _num_people _poses _images ))

(defmethod mp_pose::pose_image
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:num_people __num_people) 0)
    ((:poses __poses) ())
    ((:images __images) ())
    )
   (send-super :init)
   (setq _header __header)
   (setq _num_people (round __num_people))
   (setq _poses __poses)
   (setq _images __images)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:num_people
   (&optional __num_people)
   (if __num_people (setq _num_people __num_people)) _num_people)
  (:poses
   (&rest __poses)
   (if (keywordp (car __poses))
       (send* _poses __poses)
     (progn
       (if __poses (setq _poses (car __poses)))
       _poses)))
  (:images
   (&rest __images)
   (if (keywordp (car __images))
       (send* _images __images)
     (progn
       (if __images (setq _images (car __images)))
       _images)))
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; uint8 _num_people
    1
    ;; mp_pose/pose[] _poses
    (apply #'+ (send-all _poses :serialization-length)) 4
    ;; sensor_msgs/Image[] _images
    (apply #'+ (send-all _images :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; uint8 _num_people
       (write-byte _num_people s)
     ;; mp_pose/pose[] _poses
     (write-long (length _poses) s)
     (dolist (elem _poses)
       (send elem :serialize s)
       )
     ;; sensor_msgs/Image[] _images
     (write-long (length _images) s)
     (dolist (elem _images)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; uint8 _num_people
     (setq _num_people (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; mp_pose/pose[] _poses
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _poses (let (r) (dotimes (i n) (push (instance mp_pose::pose :init) r)) r))
     (dolist (elem- _poses)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;; sensor_msgs/Image[] _images
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _images (let (r) (dotimes (i n) (push (instance sensor_msgs::Image :init) r)) r))
     (dolist (elem- _images)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get mp_pose::pose_image :md5sum-) "55d4a4399f78dd7e19fd91e7fed0b93f")
(setf (get mp_pose::pose_image :datatype-) "mp_pose/pose_image")
(setf (get mp_pose::pose_image :definition-)
      "# Header
std_msgs/Header header

#Data
uint8 num_people
pose[] poses
sensor_msgs/Image[] images
================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: mp_pose/pose
landmark[] local_landmarks
landmark[] global_landmarks
================================================================================
MSG: mp_pose/landmark
float32 x
float32 y
float32 z 
float32 visibility
float32 presence
# int32 keypoint
================================================================================
MSG: sensor_msgs/Image
# This message contains an uncompressed image
# (0, 0) is at top-left corner of image
#

Header header        # Header timestamp should be acquisition time of image
                     # Header frame_id should be optical frame of camera
                     # origin of frame should be optical center of camera
                     # +x should point to the right in the image
                     # +y should point down in the image
                     # +z should point into to plane of the image
                     # If the frame_id here and the frame_id of the CameraInfo
                     # message associated with the image conflict
                     # the behavior is undefined

uint32 height         # image height, that is, number of rows
uint32 width          # image width, that is, number of columns

# The legal values for encoding are in file src/image_encodings.cpp
# If you want to standardize a new string format, join
# ros-users@lists.sourceforge.net and send an email proposing a new encoding.

string encoding       # Encoding of pixels -- channel meaning, ordering, size
                      # taken from the list of strings in include/sensor_msgs/image_encodings.h

uint8 is_bigendian    # is this data bigendian?
uint32 step           # Full row length in bytes
uint8[] data          # actual matrix data, size is (step * rows)

")



(provide :mp_pose/pose_image "55d4a4399f78dd7e19fd91e7fed0b93f")


