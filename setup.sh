#!/usr/bin/env bash
ENV_NAME="hri"
source $(conda info --base)/etc/profile.d/conda.sh
conda activate $ENV_NAME

source ./devel/setup.bash