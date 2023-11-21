; Auto-generated. Do not edit!


(cl:in-package mp_pose-msg)


;//! \htmlinclude pose_image.msg.html

(cl:defclass <pose_image> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (num_people
    :reader num_people
    :initarg :num_people
    :type cl:fixnum
    :initform 0)
   (poses
    :reader poses
    :initarg :poses
    :type (cl:vector mp_pose-msg:pose)
   :initform (cl:make-array 0 :element-type 'mp_pose-msg:pose :initial-element (cl:make-instance 'mp_pose-msg:pose)))
   (images
    :reader images
    :initarg :images
    :type (cl:vector sensor_msgs-msg:Image)
   :initform (cl:make-array 0 :element-type 'sensor_msgs-msg:Image :initial-element (cl:make-instance 'sensor_msgs-msg:Image))))
)

(cl:defclass pose_image (<pose_image>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <pose_image>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'pose_image)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name mp_pose-msg:<pose_image> is deprecated: use mp_pose-msg:pose_image instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <pose_image>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mp_pose-msg:header-val is deprecated.  Use mp_pose-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'num_people-val :lambda-list '(m))
(cl:defmethod num_people-val ((m <pose_image>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mp_pose-msg:num_people-val is deprecated.  Use mp_pose-msg:num_people instead.")
  (num_people m))

(cl:ensure-generic-function 'poses-val :lambda-list '(m))
(cl:defmethod poses-val ((m <pose_image>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mp_pose-msg:poses-val is deprecated.  Use mp_pose-msg:poses instead.")
  (poses m))

(cl:ensure-generic-function 'images-val :lambda-list '(m))
(cl:defmethod images-val ((m <pose_image>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mp_pose-msg:images-val is deprecated.  Use mp_pose-msg:images instead.")
  (images m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <pose_image>) ostream)
  "Serializes a message object of type '<pose_image>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'num_people)) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'poses))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'poses))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'images))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'images))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <pose_image>) istream)
  "Deserializes a message object of type '<pose_image>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'num_people)) (cl:read-byte istream))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'poses) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'poses)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'mp_pose-msg:pose))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'images) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'images)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'sensor_msgs-msg:Image))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<pose_image>)))
  "Returns string type for a message object of type '<pose_image>"
  "mp_pose/pose_image")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'pose_image)))
  "Returns string type for a message object of type 'pose_image"
  "mp_pose/pose_image")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<pose_image>)))
  "Returns md5sum for a message object of type '<pose_image>"
  "55d4a4399f78dd7e19fd91e7fed0b93f")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'pose_image)))
  "Returns md5sum for a message object of type 'pose_image"
  "55d4a4399f78dd7e19fd91e7fed0b93f")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<pose_image>)))
  "Returns full string definition for message of type '<pose_image>"
  (cl:format cl:nil "# Header~%std_msgs/Header header~%~%#Data~%uint8 num_people~%pose[] poses~%sensor_msgs/Image[] images~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: mp_pose/pose~%landmark[] local_landmarks~%landmark[] global_landmarks~%================================================================================~%MSG: mp_pose/landmark~%float32 x~%float32 y~%float32 z ~%float32 visibility~%float32 presence~%# int32 keypoint~%================================================================================~%MSG: sensor_msgs/Image~%# This message contains an uncompressed image~%# (0, 0) is at top-left corner of image~%#~%~%Header header        # Header timestamp should be acquisition time of image~%                     # Header frame_id should be optical frame of camera~%                     # origin of frame should be optical center of camera~%                     # +x should point to the right in the image~%                     # +y should point down in the image~%                     # +z should point into to plane of the image~%                     # If the frame_id here and the frame_id of the CameraInfo~%                     # message associated with the image conflict~%                     # the behavior is undefined~%~%uint32 height         # image height, that is, number of rows~%uint32 width          # image width, that is, number of columns~%~%# The legal values for encoding are in file src/image_encodings.cpp~%# If you want to standardize a new string format, join~%# ros-users@lists.sourceforge.net and send an email proposing a new encoding.~%~%string encoding       # Encoding of pixels -- channel meaning, ordering, size~%                      # taken from the list of strings in include/sensor_msgs/image_encodings.h~%~%uint8 is_bigendian    # is this data bigendian?~%uint32 step           # Full row length in bytes~%uint8[] data          # actual matrix data, size is (step * rows)~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'pose_image)))
  "Returns full string definition for message of type 'pose_image"
  (cl:format cl:nil "# Header~%std_msgs/Header header~%~%#Data~%uint8 num_people~%pose[] poses~%sensor_msgs/Image[] images~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: mp_pose/pose~%landmark[] local_landmarks~%landmark[] global_landmarks~%================================================================================~%MSG: mp_pose/landmark~%float32 x~%float32 y~%float32 z ~%float32 visibility~%float32 presence~%# int32 keypoint~%================================================================================~%MSG: sensor_msgs/Image~%# This message contains an uncompressed image~%# (0, 0) is at top-left corner of image~%#~%~%Header header        # Header timestamp should be acquisition time of image~%                     # Header frame_id should be optical frame of camera~%                     # origin of frame should be optical center of camera~%                     # +x should point to the right in the image~%                     # +y should point down in the image~%                     # +z should point into to plane of the image~%                     # If the frame_id here and the frame_id of the CameraInfo~%                     # message associated with the image conflict~%                     # the behavior is undefined~%~%uint32 height         # image height, that is, number of rows~%uint32 width          # image width, that is, number of columns~%~%# The legal values for encoding are in file src/image_encodings.cpp~%# If you want to standardize a new string format, join~%# ros-users@lists.sourceforge.net and send an email proposing a new encoding.~%~%string encoding       # Encoding of pixels -- channel meaning, ordering, size~%                      # taken from the list of strings in include/sensor_msgs/image_encodings.h~%~%uint8 is_bigendian    # is this data bigendian?~%uint32 step           # Full row length in bytes~%uint8[] data          # actual matrix data, size is (step * rows)~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <pose_image>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     1
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'poses) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'images) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <pose_image>))
  "Converts a ROS message object to a list"
  (cl:list 'pose_image
    (cl:cons ':header (header msg))
    (cl:cons ':num_people (num_people msg))
    (cl:cons ':poses (poses msg))
    (cl:cons ':images (images msg))
))
