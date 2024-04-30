#!/usr/bin/env bash
ENV_NAME="hri"
source $(conda info --base)/etc/profile.d/conda.sh
conda activate $ENV_NAME

source ./devel/setup.bash

# If any peramiters are given, launch the file
file=$(rospack find spot_hri)/src/launch.py
if [ -n "$1" ]; then
    python3 $file
fi