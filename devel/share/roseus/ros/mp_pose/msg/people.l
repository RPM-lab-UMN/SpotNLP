;; Auto-generated. Do not edit!


(when (boundp 'mp_pose::people)
  (if (not (find-package "MP_POSE"))
    (make-package "MP_POSE"))
  (shadow 'people (find-package "MP_POSE")))
(unless (find-package "MP_POSE::PEOPLE")
  (make-package "MP_POSE::PEOPLE"))

(in-package "ROS")
;;//! \htmlinclude people.msg.html
(if (not (find-package "SENSOR_MSGS"))
  (ros::roseus-add-msgs "sensor_msgs"))
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass mp_pose::people
  :super ros::object
  :slots (_header _num_people _people _color _depth ))

(defmethod mp_pose::people
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:num_people __num_people) 0)
    ((:people __people) ())
    ((:color __color) (instance sensor_msgs::Image :init))
    ((:depth __depth) (instance sensor_msgs::Image :init))
    )
   (send-super :init)
   (setq _header __header)
   (setq _num_people (round __num_people))
   (setq _people __people)
   (setq _color __color)
   (setq _depth __depth)
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
  (:people
   (&rest __people)
   (if (keywordp (car __people))
       (send* _people __people)
     (progn
       (if __people (setq _people (car __people)))
       _people)))
  (:color
   (&rest __color)
   (if (keywordp (car __color))
       (send* _color __color)
     (progn
       (if __color (setq _color (car __color)))
       _color)))
  (:depth
   (&rest __depth)
   (if (keywordp (car __depth))
       (send* _depth __depth)
     (progn
       (if __depth (setq _depth (car __depth)))
       _depth)))
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; uint8 _num_people
    1
    ;; mp_pose/person[] _people
    (apply #'+ (send-all _people :serialization-length)) 4
    ;; sensor_msgs/Image _color
    (send _color :serialization-length)
    ;; sensor_msgs/Image _depth
    (send _depth :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; uint8 _num_people
       (write-byte _num_people s)
     ;; mp_pose/person[] _people
     (write-long (length _people) s)
     (dolist (elem _people)
       (send elem :serialize s)
       )
     ;; sensor_msgs/Image _color
       (send _color :serialize s)
     ;; sensor_msgs/Image _depth
       (send _depth :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; uint8 _num_people
     (setq _num_people (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; mp_pose/person[] _people
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _people (let (r) (dotimes (i n) (push (instance mp_pose::person :init) r)) r))
     (dolist (elem- _people)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;; sensor_msgs/Image _color
     (send _color :deserialize buf ptr-) (incf ptr- (send _color :serialization-length))
   ;; sensor_msgs/Image _depth
     (send _depth :deserialize buf ptr-) (incf ptr- (send _depth :serialization-length))
   ;;
   self)
  )

(setf (get mp_pose::people :md5sum-) "4260834ec0a1895f6f8d6d7fa6c0807f")
(setf (get mp_pose::people :datatype-) "mp_pose/people")
(setf (get mp_pose::people :definition-)
      "# Header
std_msgs/Header header

#Data
uint8 num_people
person[] people
sensor_msgs/Image color
sensor_msgs/Image depth
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
MSG: mp_pose/person
# Header
std_msgs/Header header

#Data
pose pose
sensor_msgs/Image image

================================================================================
MSG: mp_pose/pose
landmark[] local_landmarks
landmark[] world_landmarks
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



(provide :mp_pose/people "4260834ec0a1895f6f8d6d7fa6c0807f")


