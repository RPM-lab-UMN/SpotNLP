
"use strict";

let landmark = require('./landmark.js');
let depth_image = require('./depth_image.js');
let pose = require('./pose.js');
let person = require('./person.js');
let people = require('./people.js');

module.exports = {
  landmark: landmark,
  depth_image: depth_image,
  pose: pose,
  person: person,
  people: people,
};
