# Spot Human Gesture Recognition


## Introduction

A NLP interface to extend SpotHRI


# OLD README


This project aims to create a robust framework for human interaction with the BostonDynamics Spot robot. The framework is based on the MediaPipe pose estimation model and XMem object tracking models. With those models, a ground truth of the human pose is created and used to train a custom gesture recognition model. The gesture recognition model is then used to control the Spot robot. The framework is designed to be modular and can be easily extended to other tasks.


## Installation

Commands:
catkin build
catkin clean 

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
