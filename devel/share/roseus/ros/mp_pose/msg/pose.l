;; Auto-generated. Do not edit!


(when (boundp 'mp_pose::pose)
  (if (not (find-package "MP_POSE"))
    (make-package "MP_POSE"))
  (shadow 'pose (find-package "MP_POSE")))
(unless (find-package "MP_POSE::POSE")
  (make-package "MP_POSE::POSE"))

(in-package "ROS")
;;//! \htmlinclude pose.msg.html


(defclass mp_pose::pose
  :super ros::object
  :slots (_local_landmarks _world_landmarks ))

(defmethod mp_pose::pose
  (:init
   (&key
    ((:local_landmarks __local_landmarks) ())
    ((:world_landmarks __world_landmarks) ())
    )
   (send-super :init)
   (setq _local_landmarks __local_landmarks)
   (setq _world_landmarks __world_landmarks)
   self)
  (:local_landmarks
   (&rest __local_landmarks)
   (if (keywordp (car __local_landmarks))
       (send* _local_landmarks __local_landmarks)
     (progn
       (if __local_landmarks (setq _local_landmarks (car __local_landmarks)))
       _local_landmarks)))
  (:world_landmarks
   (&rest __world_landmarks)
   (if (keywordp (car __world_landmarks))
       (send* _world_landmarks __world_landmarks)
     (progn
       (if __world_landmarks (setq _world_landmarks (car __world_landmarks)))
       _world_landmarks)))
  (:serialization-length
   ()
   (+
    ;; mp_pose/landmark[] _local_landmarks
    (apply #'+ (send-all _local_landmarks :serialization-length)) 4
    ;; mp_pose/landmark[] _world_landmarks
    (apply #'+ (send-all _world_landmarks :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; mp_pose/landmark[] _local_landmarks
     (write-long (length _local_landmarks) s)
     (dolist (elem _local_landmarks)
       (send elem :serialize s)
       )
     ;; mp_pose/landmark[] _world_landmarks
     (write-long (length _world_landmarks) s)
     (dolist (elem _world_landmarks)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; mp_pose/landmark[] _local_landmarks
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _local_landmarks (let (r) (dotimes (i n) (push (instance mp_pose::landmark :init) r)) r))
     (dolist (elem- _local_landmarks)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;; mp_pose/landmark[] _world_landmarks
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _world_landmarks (let (r) (dotimes (i n) (push (instance mp_pose::landmark :init) r)) r))
     (dolist (elem- _world_landmarks)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get mp_pose::pose :md5sum-) "42088b21d60401ab7b2e8c479a8fd9b2")
(setf (get mp_pose::pose :datatype-) "mp_pose/pose")
(setf (get mp_pose::pose :definition-)
      "landmark[] local_landmarks
landmark[] world_landmarks
================================================================================
MSG: mp_pose/landmark
float32 x
float32 y
float32 z 
float32 visibility
float32 presence
# int32 keypoint
")



(provide :mp_pose/pose "42088b21d60401ab7b2e8c479a8fd9b2")


