; Auto-generated. Do not edit!


(cl:in-package mp_pose-msg)


;//! \htmlinclude landmark.msg.html

(cl:defclass <landmark> (roslisp-msg-protocol:ros-message)
  ((x
    :reader x
    :initarg :x
    :type cl:float
    :initform 0.0)
   (y
    :reader y
    :initarg :y
    :type cl:float
    :initform 0.0)
   (z
    :reader z
    :initarg :z
    :type cl:float
    :initform 0.0)
   (visibility
    :reader visibility
    :initarg :visibility
    :type cl:float
    :initform 0.0)
   (presence
    :reader presence
    :initarg :presence
    :type cl:float
    :initform 0.0))
)

(cl:defclass landmark (<landmark>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <landmark>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'landmark)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name mp_pose-msg:<landmark> is deprecated: use mp_pose-msg:landmark instead.")))

(cl:ensure-generic-function 'x-val :lambda-list '(m))
(cl:defmethod x-val ((m <landmark>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mp_pose-msg:x-val is deprecated.  Use mp_pose-msg:x instead.")
  (x m))

(cl:ensure-generic-function 'y-val :lambda-list '(m))
(cl:defmethod y-val ((m <landmark>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mp_pose-msg:y-val is deprecated.  Use mp_pose-msg:y instead.")
  (y m))

(cl:ensure-generic-function 'z-val :lambda-list '(m))
(cl:defmethod z-val ((m <landmark>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mp_pose-msg:z-val is deprecated.  Use mp_pose-msg:z instead.")
  (z m))

(cl:ensure-generic-function 'visibility-val :lambda-list '(m))
(cl:defmethod visibility-val ((m <landmark>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mp_pose-msg:visibility-val is deprecated.  Use mp_pose-msg:visibility instead.")
  (visibility m))

(cl:ensure-generic-function 'presence-val :lambda-list '(m))
(cl:defmethod presence-val ((m <landmark>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mp_pose-msg:presence-val is deprecated.  Use mp_pose-msg:presence instead.")
  (presence m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <landmark>) ostream)
  "Serializes a message object of type '<landmark>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'z))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'visibility))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'presence))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <landmark>) istream)
  "Deserializes a message object of type '<landmark>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'x) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'y) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'z) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'visibility) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'presence) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<landmark>)))
  "Returns string type for a message object of type '<landmark>"
  "mp_pose/landmark")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'landmark)))
  "Returns string type for a message object of type 'landmark"
  "mp_pose/landmark")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<landmark>)))
  "Returns md5sum for a message object of type '<landmark>"
  "0679b968d5e29e39a4e5b5b3f281f78a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'landmark)))
  "Returns md5sum for a message object of type 'landmark"
  "0679b968d5e29e39a4e5b5b3f281f78a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<landmark>)))
  "Returns full string definition for message of type '<landmark>"
  (cl:format cl:nil "float32 x~%float32 y~%float32 z ~%float32 visibility~%float32 presence~%# int32 keypoint~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'landmark)))
  "Returns full string definition for message of type 'landmark"
  (cl:format cl:nil "float32 x~%float32 y~%float32 z ~%float32 visibility~%float32 presence~%# int32 keypoint~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <landmark>))
  (cl:+ 0
     4
     4
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <landmark>))
  "Converts a ROS message object to a list"
  (cl:list 'landmark
    (cl:cons ':x (x msg))
    (cl:cons ':y (y msg))
    (cl:cons ':z (z msg))
    (cl:cons ':visibility (visibility msg))
    (cl:cons ':presence (presence msg))
))
