// Auto-generated. Do not edit!

// (in-package mp_pose.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let landmark = require('./landmark.js');

//-----------------------------------------------------------

class pose {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.local_landmarks = null;
      this.world_landmarks = null;
    }
    else {
      if (initObj.hasOwnProperty('local_landmarks')) {
        this.local_landmarks = initObj.local_landmarks
      }
      else {
        this.local_landmarks = [];
      }
      if (initObj.hasOwnProperty('world_landmarks')) {
        this.world_landmarks = initObj.world_landmarks
      }
      else {
        this.world_landmarks = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type pose
    // Serialize message field [local_landmarks]
    // Serialize the length for message field [local_landmarks]
    bufferOffset = _serializer.uint32(obj.local_landmarks.length, buffer, bufferOffset);
    obj.local_landmarks.forEach((val) => {
      bufferOffset = landmark.serialize(val, buffer, bufferOffset);
    });
    // Serialize message field [world_landmarks]
    // Serialize the length for message field [world_landmarks]
    bufferOffset = _serializer.uint32(obj.world_landmarks.length, buffer, bufferOffset);
    obj.world_landmarks.forEach((val) => {
      bufferOffset = landmark.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type pose
    let len;
    let data = new pose(null);
    // Deserialize message field [local_landmarks]
    // Deserialize array length for message field [local_landmarks]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.local_landmarks = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.local_landmarks[i] = landmark.deserialize(buffer, bufferOffset)
    }
    // Deserialize message field [world_landmarks]
    // Deserialize array length for message field [world_landmarks]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.world_landmarks = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.world_landmarks[i] = landmark.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 20 * object.local_landmarks.length;
    length += 20 * object.world_landmarks.length;
    return length + 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'mp_pose/pose';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '42088b21d60401ab7b2e8c479a8fd9b2';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
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
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new pose(null);
    if (msg.local_landmarks !== undefined) {
      resolved.local_landmarks = new Array(msg.local_landmarks.length);
      for (let i = 0; i < resolved.local_landmarks.length; ++i) {
        resolved.local_landmarks[i] = landmark.Resolve(msg.local_landmarks[i]);
      }
    }
    else {
      resolved.local_landmarks = []
    }

    if (msg.world_landmarks !== undefined) {
      resolved.world_landmarks = new Array(msg.world_landmarks.length);
      for (let i = 0; i < resolved.world_landmarks.length; ++i) {
        resolved.world_landmarks[i] = landmark.Resolve(msg.world_landmarks[i]);
      }
    }
    else {
      resolved.world_landmarks = []
    }

    return resolved;
    }
};

module.exports = pose;
