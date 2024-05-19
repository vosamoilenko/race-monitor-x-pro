#!/bin/bash
echo "starting up"

export PATH="/home/pi/miniforge3/bin:$PATH"

source /home/pi/miniforge3/etc/profile.d/conda.sh

conda activate py27 > text.txt

which python >> text.txt

python /home/pi/Developer/py/obd-rally-golf/index.py
