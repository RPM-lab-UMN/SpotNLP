# Spot Human Gesture Recognition


## Introduction


This project aims to create a robust framework for human interaction with the BostonDynamics Spot robot. The framework is based on the MediaPipe pose estimation model and XMem object tracking models. With those models, a ground truth of the human pose is created and used to train a custom gesture recognition model. The gesture recognition model is then used to control the Spot robot. The framework is designed to be modular and can be easily extended to other tasks.


## Installation


TTS:
```apt install espeak```


Mamba Environment:
```mamba env create -f environment.yml```
activate, and then ```pip install git+https://github.com/cheind/py-thin-plate-spline```.


XMem:
Run ```model.sh``` from its local directory. 


MediaPipe:
The wieghts are preinstalled, and there are dependencies in the environment.yml. No Acions needed.



## Usage


**Note: This system is best used on a system with a CUDA-capable GPU. This is not mandatory, but performance will suffer heavily to the point of being unusable. Ubuntu, or at least GNU/Linux, may be necessary. Also, this may conflict if ROS is already installed.**


To run, first source build using ```catkin build``` and then ```setup.sh``` in the root directory. Then run [```/src/spot_hri/src/launch.py```](/src/spot_hri/src/launch.py) with ```python3```. Assuming all the hardware is present, Spot should be ready to pair with a leader and start following. 



## Structure


Most of the codebase for this project is novel, with some XMem code for executing their model. This project is structured as a ROS Noetic project. 


The [```/src```](/src/) folder holds all the individual packages:


### Core Pipeline
- [`/src/camera`](/src/camera): This contains code to access either an Intel RealSense camera, or the BostonDynamics Spot Gripper camera.
 - [`/src/mp_pose`](/src/mp_pose): This folder contains code to run infrence on Google's MediaPipe Pose. It also holds all message definitions. 
 - [`/src/xmem`](/src/xmem): This holds the XMem code, the wieghts must be installed before use. 
 - [`/src/gesture`](/src/gesture): This holds the buffer code.
 - [`/src/model`](/src/model): This package represents the gesture classifier. New classifiers should be used in place of this.
 - [`/src/state_core`](/src/state_core): This holds code relating to state transitions and the state machine. Modify for adapting to new applications.
 - [`/src/movement_core`](/src/movement_core): This is responsible for the kinematics of Spot's movements.
 - [`/src/tts`](/src/tts): This package runs a TTS engine to announce state changes
 - [`/src/spot_hri`](/src/spot_hri): This is the home of the launch file to run the system. Modify this to launch other files. 


### Development Code
 - [`/src/mp_pose`](/src/mp_pose): Additional message types should go here.
 - [`/src/model`](/src/model): New gesture classifier models should go in this package. Training code is provided to load the dataset. 
 - [`/src/gesture`](/src/gesture): Code for recording and labeling data. 
 - [`/src/spot_hri`](/src/spot_hri): This holds log files from the subprocess during a run.