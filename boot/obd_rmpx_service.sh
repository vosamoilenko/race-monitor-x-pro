#!/bin/bash

export PATH="/home/pi/miniforge3/bin:$PATH"

source /home/pi/miniforge3/etc/profile.d/conda.sh

conda activate obd-py-3

which python

sleep 30

python /home/pi/Developer/py/obd-rally-golf/index.obd.py
