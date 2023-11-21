# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "mp_pose: 5 messages, 0 services")

set(MSG_I_FLAGS "-Imp_pose:/home/adam/HRI/src/mp_pose/msg;-Istd_msgs:/home/adam/mambaforge/envs/hri/share/std_msgs/cmake/../msg;-Isensor_msgs:/home/adam/mambaforge/envs/hri/share/sensor_msgs/cmake/../msg;-Igeometry_msgs:/home/adam/mambaforge/envs/hri/share/geometry_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(mp_pose_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/landmark.msg" NAME_WE)
add_custom_target(_mp_pose_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "mp_pose" "/home/adam/HRI/src/mp_pose/msg/landmark.msg" ""
)

get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/pose.msg" NAME_WE)
add_custom_target(_mp_pose_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "mp_pose" "/home/adam/HRI/src/mp_pose/msg/pose.msg" "mp_pose/landmark"
)

get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/person.msg" NAME_WE)
add_custom_target(_mp_pose_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "mp_pose" "/home/adam/HRI/src/mp_pose/msg/person.msg" "sensor_msgs/Image:mp_pose/landmark:std_msgs/Header:mp_pose/pose"
)

get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/people.msg" NAME_WE)
add_custom_target(_mp_pose_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "mp_pose" "/home/adam/HRI/src/mp_pose/msg/people.msg" "sensor_msgs/Image:mp_pose/pose:std_msgs/Header:mp_pose/landmark:mp_pose/person"
)

get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/depth_image.msg" NAME_WE)
add_custom_target(_mp_pose_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "mp_pose" "/home/adam/HRI/src/mp_pose/msg/depth_image.msg" "sensor_msgs/Image:std_msgs/Header"
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/landmark.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/mp_pose
)
_generate_msg_cpp(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/pose.msg"
  "${MSG_I_FLAGS}"
  "/home/adam/HRI/src/mp_pose/msg/landmark.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/mp_pose
)
_generate_msg_cpp(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/person.msg"
  "${MSG_I_FLAGS}"
  "/home/adam/mambaforge/envs/hri/share/sensor_msgs/cmake/../msg/Image.msg;/home/adam/HRI/src/mp_pose/msg/landmark.msg;/home/adam/mambaforge/envs/hri/share/std_msgs/cmake/../msg/Header.msg;/home/adam/HRI/src/mp_pose/msg/pose.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/mp_pose
)
_generate_msg_cpp(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/people.msg"
  "${MSG_I_FLAGS}"
  "/home/adam/mambaforge/envs/hri/share/sensor_msgs/cmake/../msg/Image.msg;/home/adam/HRI/src/mp_pose/msg/pose.msg;/home/adam/mambaforge/envs/hri/share/std_msgs/cmake/../msg/Header.msg;/home/adam/HRI/src/mp_pose/msg/landmark.msg;/home/adam/HRI/src/mp_pose/msg/person.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/mp_pose
)
_generate_msg_cpp(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/depth_image.msg"
  "${MSG_I_FLAGS}"
  "/home/adam/mambaforge/envs/hri/share/sensor_msgs/cmake/../msg/Image.msg;/home/adam/mambaforge/envs/hri/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/mp_pose
)

### Generating Services

### Generating Module File
_generate_module_cpp(mp_pose
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/mp_pose
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(mp_pose_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(mp_pose_generate_messages mp_pose_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/landmark.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_cpp _mp_pose_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/pose.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_cpp _mp_pose_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/person.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_cpp _mp_pose_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/people.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_cpp _mp_pose_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/depth_image.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_cpp _mp_pose_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(mp_pose_gencpp)
add_dependencies(mp_pose_gencpp mp_pose_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS mp_pose_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/landmark.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/mp_pose
)
_generate_msg_eus(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/pose.msg"
  "${MSG_I_FLAGS}"
  "/home/adam/HRI/src/mp_pose/msg/landmark.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/mp_pose
)
_generate_msg_eus(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/person.msg"
  "${MSG_I_FLAGS}"
  "/home/adam/mambaforge/envs/hri/share/sensor_msgs/cmake/../msg/Image.msg;/home/adam/HRI/src/mp_pose/msg/landmark.msg;/home/adam/mambaforge/envs/hri/share/std_msgs/cmake/../msg/Header.msg;/home/adam/HRI/src/mp_pose/msg/pose.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/mp_pose
)
_generate_msg_eus(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/people.msg"
  "${MSG_I_FLAGS}"
  "/home/adam/mambaforge/envs/hri/share/sensor_msgs/cmake/../msg/Image.msg;/home/adam/HRI/src/mp_pose/msg/pose.msg;/home/adam/mambaforge/envs/hri/share/std_msgs/cmake/../msg/Header.msg;/home/adam/HRI/src/mp_pose/msg/landmark.msg;/home/adam/HRI/src/mp_pose/msg/person.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/mp_pose
)
_generate_msg_eus(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/depth_image.msg"
  "${MSG_I_FLAGS}"
  "/home/adam/mambaforge/envs/hri/share/sensor_msgs/cmake/../msg/Image.msg;/home/adam/mambaforge/envs/hri/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/mp_pose
)

### Generating Services

### Generating Module File
_generate_module_eus(mp_pose
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/mp_pose
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(mp_pose_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(mp_pose_generate_messages mp_pose_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/landmark.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_eus _mp_pose_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/pose.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_eus _mp_pose_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/person.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_eus _mp_pose_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/people.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_eus _mp_pose_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/depth_image.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_eus _mp_pose_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(mp_pose_geneus)
add_dependencies(mp_pose_geneus mp_pose_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS mp_pose_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/landmark.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/mp_pose
)
_generate_msg_lisp(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/pose.msg"
  "${MSG_I_FLAGS}"
  "/home/adam/HRI/src/mp_pose/msg/landmark.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/mp_pose
)
_generate_msg_lisp(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/person.msg"
  "${MSG_I_FLAGS}"
  "/home/adam/mambaforge/envs/hri/share/sensor_msgs/cmake/../msg/Image.msg;/home/adam/HRI/src/mp_pose/msg/landmark.msg;/home/adam/mambaforge/envs/hri/share/std_msgs/cmake/../msg/Header.msg;/home/adam/HRI/src/mp_pose/msg/pose.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/mp_pose
)
_generate_msg_lisp(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/people.msg"
  "${MSG_I_FLAGS}"
  "/home/adam/mambaforge/envs/hri/share/sensor_msgs/cmake/../msg/Image.msg;/home/adam/HRI/src/mp_pose/msg/pose.msg;/home/adam/mambaforge/envs/hri/share/std_msgs/cmake/../msg/Header.msg;/home/adam/HRI/src/mp_pose/msg/landmark.msg;/home/adam/HRI/src/mp_pose/msg/person.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/mp_pose
)
_generate_msg_lisp(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/depth_image.msg"
  "${MSG_I_FLAGS}"
  "/home/adam/mambaforge/envs/hri/share/sensor_msgs/cmake/../msg/Image.msg;/home/adam/mambaforge/envs/hri/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/mp_pose
)

### Generating Services

### Generating Module File
_generate_module_lisp(mp_pose
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/mp_pose
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(mp_pose_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(mp_pose_generate_messages mp_pose_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/landmark.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_lisp _mp_pose_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/pose.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_lisp _mp_pose_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/person.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_lisp _mp_pose_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/people.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_lisp _mp_pose_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/depth_image.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_lisp _mp_pose_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(mp_pose_genlisp)
add_dependencies(mp_pose_genlisp mp_pose_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS mp_pose_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/landmark.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/mp_pose
)
_generate_msg_nodejs(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/pose.msg"
  "${MSG_I_FLAGS}"
  "/home/adam/HRI/src/mp_pose/msg/landmark.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/mp_pose
)
_generate_msg_nodejs(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/person.msg"
  "${MSG_I_FLAGS}"
  "/home/adam/mambaforge/envs/hri/share/sensor_msgs/cmake/../msg/Image.msg;/home/adam/HRI/src/mp_pose/msg/landmark.msg;/home/adam/mambaforge/envs/hri/share/std_msgs/cmake/../msg/Header.msg;/home/adam/HRI/src/mp_pose/msg/pose.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/mp_pose
)
_generate_msg_nodejs(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/people.msg"
  "${MSG_I_FLAGS}"
  "/home/adam/mambaforge/envs/hri/share/sensor_msgs/cmake/../msg/Image.msg;/home/adam/HRI/src/mp_pose/msg/pose.msg;/home/adam/mambaforge/envs/hri/share/std_msgs/cmake/../msg/Header.msg;/home/adam/HRI/src/mp_pose/msg/landmark.msg;/home/adam/HRI/src/mp_pose/msg/person.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/mp_pose
)
_generate_msg_nodejs(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/depth_image.msg"
  "${MSG_I_FLAGS}"
  "/home/adam/mambaforge/envs/hri/share/sensor_msgs/cmake/../msg/Image.msg;/home/adam/mambaforge/envs/hri/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/mp_pose
)

### Generating Services

### Generating Module File
_generate_module_nodejs(mp_pose
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/mp_pose
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(mp_pose_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(mp_pose_generate_messages mp_pose_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/landmark.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_nodejs _mp_pose_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/pose.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_nodejs _mp_pose_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/person.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_nodejs _mp_pose_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/people.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_nodejs _mp_pose_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/depth_image.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_nodejs _mp_pose_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(mp_pose_gennodejs)
add_dependencies(mp_pose_gennodejs mp_pose_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS mp_pose_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/landmark.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/mp_pose
)
_generate_msg_py(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/pose.msg"
  "${MSG_I_FLAGS}"
  "/home/adam/HRI/src/mp_pose/msg/landmark.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/mp_pose
)
_generate_msg_py(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/person.msg"
  "${MSG_I_FLAGS}"
  "/home/adam/mambaforge/envs/hri/share/sensor_msgs/cmake/../msg/Image.msg;/home/adam/HRI/src/mp_pose/msg/landmark.msg;/home/adam/mambaforge/envs/hri/share/std_msgs/cmake/../msg/Header.msg;/home/adam/HRI/src/mp_pose/msg/pose.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/mp_pose
)
_generate_msg_py(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/people.msg"
  "${MSG_I_FLAGS}"
  "/home/adam/mambaforge/envs/hri/share/sensor_msgs/cmake/../msg/Image.msg;/home/adam/HRI/src/mp_pose/msg/pose.msg;/home/adam/mambaforge/envs/hri/share/std_msgs/cmake/../msg/Header.msg;/home/adam/HRI/src/mp_pose/msg/landmark.msg;/home/adam/HRI/src/mp_pose/msg/person.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/mp_pose
)
_generate_msg_py(mp_pose
  "/home/adam/HRI/src/mp_pose/msg/depth_image.msg"
  "${MSG_I_FLAGS}"
  "/home/adam/mambaforge/envs/hri/share/sensor_msgs/cmake/../msg/Image.msg;/home/adam/mambaforge/envs/hri/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/mp_pose
)

### Generating Services

### Generating Module File
_generate_module_py(mp_pose
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/mp_pose
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(mp_pose_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(mp_pose_generate_messages mp_pose_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/landmark.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_py _mp_pose_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/pose.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_py _mp_pose_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/person.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_py _mp_pose_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/people.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_py _mp_pose_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/adam/HRI/src/mp_pose/msg/depth_image.msg" NAME_WE)
add_dependencies(mp_pose_generate_messages_py _mp_pose_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(mp_pose_genpy)
add_dependencies(mp_pose_genpy mp_pose_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS mp_pose_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/mp_pose)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/mp_pose
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(mp_pose_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()
if(TARGET sensor_msgs_generate_messages_cpp)
  add_dependencies(mp_pose_generate_messages_cpp sensor_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/mp_pose)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/mp_pose
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(mp_pose_generate_messages_eus std_msgs_generate_messages_eus)
endif()
if(TARGET sensor_msgs_generate_messages_eus)
  add_dependencies(mp_pose_generate_messages_eus sensor_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/mp_pose)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/mp_pose
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(mp_pose_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()
if(TARGET sensor_msgs_generate_messages_lisp)
  add_dependencies(mp_pose_generate_messages_lisp sensor_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/mp_pose)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/mp_pose
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(mp_pose_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()
if(TARGET sensor_msgs_generate_messages_nodejs)
  add_dependencies(mp_pose_generate_messages_nodejs sensor_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/mp_pose)
  install(CODE "execute_process(COMMAND \"/home/adam/mambaforge/envs/hri/bin/python3.9\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/mp_pose\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/mp_pose
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(mp_pose_generate_messages_py std_msgs_generate_messages_py)
endif()
if(TARGET sensor_msgs_generate_messages_py)
  add_dependencies(mp_pose_generate_messages_py sensor_msgs_generate_messages_py)
endif()
