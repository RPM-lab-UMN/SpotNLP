; Auto-generated. Do not edit!


(cl:in-package mp_pose-msg)


;//! \htmlinclude pose.msg.html

(cl:defclass <pose> (roslisp-msg-protocol:ros-message)
  ((local_landmarks
    :reader local_landmarks
    :initarg :local_landmarks
    :type (cl:vector mp_pose-msg:landmark)
   :initform (cl:make-array 0 :element-type 'mp_pose-msg:landmark :initial-element (cl:make-instance 'mp_pose-msg:landmark)))
   (world_landmarks
    :reader world_landmarks
    :initarg :world_landmarks
    :type (cl:vector mp_pose-msg:landmark)
   :initform (cl:make-array 0 :element-type 'mp_pose-msg:landmark :initial-element (cl:make-instance 'mp_pose-msg:landmark))))
)

(cl:defclass pose (<pose>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <pose>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'pose)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name mp_pose-msg:<pose> is deprecated: use mp_pose-msg:pose instead.")))

(cl:ensure-generic-function 'local_landmarks-val :lambda-list '(m))
(cl:defmethod local_landmarks-val ((m <pose>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mp_pose-msg:local_landmarks-val is deprecated.  Use mp_pose-msg:local_landmarks instead.")
  (local_landmarks m))

(cl:ensure-generic-function 'world_landmarks-val :lambda-list '(m))
(cl:defmethod world_landmarks-val ((m <pose>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mp_pose-msg:world_landmarks-val is deprecated.  Use mp_pose-msg:world_landmarks instead.")
  (world_landmarks m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <pose>) ostream)
  "Serializes a message object of type '<pose>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'local_landmarks))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'local_landmarks))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'world_landmarks))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'world_landmarks))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <pose>) istream)
  "Deserializes a message object of type '<pose>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'local_landmarks) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'local_landmarks)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'mp_pose-msg:landmark))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'world_landmarks) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'world_landmarks)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'mp_pose-msg:landmark))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<pose>)))
  "Returns string type for a message object of type '<pose>"
  "mp_pose/pose")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'pose)))
  "Returns string type for a message object of type 'pose"
  "mp_pose/pose")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<pose>)))
  "Returns md5sum for a message object of type '<pose>"
  "42088b21d60401ab7b2e8c479a8fd9b2")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'pose)))
  "Returns md5sum for a message object of type 'pose"
  "42088b21d60401ab7b2e8c479a8fd9b2")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<pose>)))
  "Returns full string definition for message of type '<pose>"
  (cl:format cl:nil "landmark[] local_landmarks~%landmark[] world_landmarks~%================================================================================~%MSG: mp_pose/landmark~%float32 x~%float32 y~%float32 z ~%float32 visibility~%float32 presence~%# int32 keypoint~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'pose)))
  "Returns full string definition for message of type 'pose"
  (cl:format cl:nil "landmark[] local_landmarks~%landmark[] world_landmarks~%================================================================================~%MSG: mp_pose/landmark~%float32 x~%float32 y~%float32 z ~%float32 visibility~%float32 presence~%# int32 keypoint~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <pose>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'local_landmarks) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'world_landmarks) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <pose>))
  "Converts a ROS message object to a list"
  (cl:list 'pose
    (cl:cons ':local_landmarks (local_landmarks msg))
    (cl:cons ':world_landmarks (world_landmarks msg))
))
