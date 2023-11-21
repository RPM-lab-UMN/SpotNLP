;; Auto-generated. Do not edit!


(when (boundp 'mp_pose::landmark)
  (if (not (find-package "MP_POSE"))
    (make-package "MP_POSE"))
  (shadow 'landmark (find-package "MP_POSE")))
(unless (find-package "MP_POSE::LANDMARK")
  (make-package "MP_POSE::LANDMARK"))

(in-package "ROS")
;;//! \htmlinclude landmark.msg.html


(defclass mp_pose::landmark
  :super ros::object
  :slots (_x _y _z _visibility _presence ))

(defmethod mp_pose::landmark
  (:init
   (&key
    ((:x __x) 0.0)
    ((:y __y) 0.0)
    ((:z __z) 0.0)
    ((:visibility __visibility) 0.0)
    ((:presence __presence) 0.0)
    )
   (send-super :init)
   (setq _x (float __x))
   (setq _y (float __y))
   (setq _z (float __z))
   (setq _visibility (float __visibility))
   (setq _presence (float __presence))
   self)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:z
   (&optional __z)
   (if __z (setq _z __z)) _z)
  (:visibility
   (&optional __visibility)
   (if __visibility (setq _visibility __visibility)) _visibility)
  (:presence
   (&optional __presence)
   (if __presence (setq _presence __presence)) _presence)
  (:serialization-length
   ()
   (+
    ;; float32 _x
    4
    ;; float32 _y
    4
    ;; float32 _z
    4
    ;; float32 _visibility
    4
    ;; float32 _presence
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _x
       (sys::poke _x (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _y
       (sys::poke _y (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _z
       (sys::poke _z (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _visibility
       (sys::poke _visibility (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _presence
       (sys::poke _presence (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _x
     (setq _x (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _y
     (setq _y (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _z
     (setq _z (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _visibility
     (setq _visibility (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _presence
     (setq _presence (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get mp_pose::landmark :md5sum-) "0679b968d5e29e39a4e5b5b3f281f78a")
(setf (get mp_pose::landmark :datatype-) "mp_pose/landmark")
(setf (get mp_pose::landmark :definition-)
      "float32 x
float32 y
float32 z 
float32 visibility
float32 presence
# int32 keypoint
")



(provide :mp_pose/landmark "0679b968d5e29e39a4e5b5b3f281f78a")


