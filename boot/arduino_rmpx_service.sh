#!/bin/bash

export PATH="/home/pi/miniforge3/bin:$PATH"

source /home/pi/miniforge3/etc/profile.d/conda.sh

conda activate obd-py-3

which python

sleep 5

python /home/pi/Developer/py/obd-rally-golf/index.arduino.py
