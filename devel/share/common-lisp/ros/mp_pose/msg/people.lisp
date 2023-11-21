; Auto-generated. Do not edit!


(cl:in-package mp_pose-msg)


;//! \htmlinclude people.msg.html

(cl:defclass <people> (roslisp-msg-protocol:ros-message)
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
   (people
    :reader people
    :initarg :people
    :type (cl:vector mp_pose-msg:person)
   :initform (cl:make-array 0 :element-type 'mp_pose-msg:person :initial-element (cl:make-instance 'mp_pose-msg:person)))
   (color
    :reader color
    :initarg :color
    :type sensor_msgs-msg:Image
    :initform (cl:make-instance 'sensor_msgs-msg:Image))
   (depth
    :reader depth
    :initarg :depth
    :type sensor_msgs-msg:Image
    :initform (cl:make-instance 'sensor_msgs-msg:Image)))
)

(cl:defclass people (<people>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <people>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'people)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name mp_pose-msg:<people> is deprecated: use mp_pose-msg:people instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <people>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mp_pose-msg:header-val is deprecated.  Use mp_pose-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'num_people-val :lambda-list '(m))
(cl:defmethod num_people-val ((m <people>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mp_pose-msg:num_people-val is deprecated.  Use mp_pose-msg:num_people instead.")
  (num_people m))

(cl:ensure-generic-function 'people-val :lambda-list '(m))
(cl:defmethod people-val ((m <people>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mp_pose-msg:people-val is deprecated.  Use mp_pose-msg:people instead.")
  (people m))

(cl:ensure-generic-function 'color-val :lambda-list '(m))
(cl:defmethod color-val ((m <people>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mp_pose-msg:color-val is deprecated.  Use mp_pose-msg:color instead.")
  (color m))

(cl:ensure-generic-function 'depth-val :lambda-list '(m))
(cl:defmethod depth-val ((m <people>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mp_pose-msg:depth-val is deprecated.  Use mp_pose-msg:depth instead.")
  (depth m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <people>) ostream)
  "Serializes a message object of type '<people>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'num_people)) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'people))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'people))
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'color) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'depth) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <people>) istream)
  "Deserializes a message object of type '<people>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'num_people)) (cl:read-byte istream))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'people) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'people)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'mp_pose-msg:person))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'color) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'depth) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<people>)))
  "Returns string type for a message object of type '<people>"
  "mp_pose/people")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'people)))
  "Returns string type for a message object of type 'people"
  "mp_pose/people")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<people>)))
  "Returns md5sum for a message object of type '<people>"
  "4260834ec0a1895f6f8d6d7fa6c0807f")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'people)))
  "Returns md5sum for a message object of type 'people"
  "4260834ec0a1895f6f8d6d7fa6c0807f")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<people>)))
  "Returns full string definition for message of type '<people>"
  (cl:format cl:nil "# Header~%std_msgs/Header header~%~%#Data~%uint8 num_people~%person[] people~%sensor_msgs/Image color~%sensor_msgs/Image depth~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: mp_pose/person~%# Header~%std_msgs/Header header~%~%#Data~%pose pose~%sensor_msgs/Image image~%~%================================================================================~%MSG: mp_pose/pose~%landmark[] local_landmarks~%landmark[] world_landmarks~%================================================================================~%MSG: mp_pose/landmark~%float32 x~%float32 y~%float32 z ~%float32 visibility~%float32 presence~%# int32 keypoint~%================================================================================~%MSG: sensor_msgs/Image~%# This message contains an uncompressed image~%# (0, 0) is at top-left corner of image~%#~%~%Header header        # Header timestamp should be acquisition time of image~%                     # Header frame_id should be optical frame of camera~%                     # origin of frame should be optical center of camera~%                     # +x should point to the right in the image~%                     # +y should point down in the image~%                     # +z should point into to plane of the image~%                     # If the frame_id here and the frame_id of the CameraInfo~%                     # message associated with the image conflict~%                     # the behavior is undefined~%~%uint32 height         # image height, that is, number of rows~%uint32 width          # image width, that is, number of columns~%~%# The legal values for encoding are in file src/image_encodings.cpp~%# If you want to standardize a new string format, join~%# ros-users@lists.sourceforge.net and send an email proposing a new encoding.~%~%string encoding       # Encoding of pixels -- channel meaning, ordering, size~%                      # taken from the list of strings in include/sensor_msgs/image_encodings.h~%~%uint8 is_bigendian    # is this data bigendian?~%uint32 step           # Full row length in bytes~%uint8[] data          # actual matrix data, size is (step * rows)~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'people)))
  "Returns full string definition for message of type 'people"
  (cl:format cl:nil "# Header~%std_msgs/Header header~%~%#Data~%uint8 num_people~%person[] people~%sensor_msgs/Image color~%sensor_msgs/Image depth~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: mp_pose/person~%# Header~%std_msgs/Header header~%~%#Data~%pose pose~%sensor_msgs/Image image~%~%================================================================================~%MSG: mp_pose/pose~%landmark[] local_landmarks~%landmark[] world_landmarks~%================================================================================~%MSG: mp_pose/landmark~%float32 x~%float32 y~%float32 z ~%float32 visibility~%float32 presence~%# int32 keypoint~%================================================================================~%MSG: sensor_msgs/Image~%# This message contains an uncompressed image~%# (0, 0) is at top-left corner of image~%#~%~%Header header        # Header timestamp should be acquisition time of image~%                     # Header frame_id should be optical frame of camera~%                     # origin of frame should be optical center of camera~%                     # +x should point to the right in the image~%                     # +y should point down in the image~%                     # +z should point into to plane of the image~%                     # If the frame_id here and the frame_id of the CameraInfo~%                     # message associated with the image conflict~%                     # the behavior is undefined~%~%uint32 height         # image height, that is, number of rows~%uint32 width          # image width, that is, number of columns~%~%# The legal values for encoding are in file src/image_encodings.cpp~%# If you want to standardize a new string format, join~%# ros-users@lists.sourceforge.net and send an email proposing a new encoding.~%~%string encoding       # Encoding of pixels -- channel meaning, ordering, size~%                      # taken from the list of strings in include/sensor_msgs/image_encodings.h~%~%uint8 is_bigendian    # is this data bigendian?~%uint32 step           # Full row length in bytes~%uint8[] data          # actual matrix data, size is (step * rows)~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <people>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     1
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'people) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'color))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'depth))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <people>))
  "Converts a ROS message object to a list"
  (cl:list 'people
    (cl:cons ':header (header msg))
    (cl:cons ':num_people (num_people msg))
    (cl:cons ':people (people msg))
    (cl:cons ':color (color msg))
    (cl:cons ':depth (depth msg))
))
