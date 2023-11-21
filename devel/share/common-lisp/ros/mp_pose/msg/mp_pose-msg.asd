
(cl:in-package :asdf)

(defsystem "mp_pose-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :sensor_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "depth_image" :depends-on ("_package_depth_image"))
    (:file "_package_depth_image" :depends-on ("_package"))
    (:file "landmark" :depends-on ("_package_landmark"))
    (:file "_package_landmark" :depends-on ("_package"))
    (:file "people" :depends-on ("_package_people"))
    (:file "_package_people" :depends-on ("_package"))
    (:file "person" :depends-on ("_package_person"))
    (:file "_package_person" :depends-on ("_package"))
    (:file "pose" :depends-on ("_package_pose"))
    (:file "_package_pose" :depends-on ("_package"))
  ))