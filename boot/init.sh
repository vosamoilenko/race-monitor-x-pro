#!/bin/bash
echo "starting up"

export PATH="/home/pi/miniforge3/bin:$PATH"

source /home/pi/miniforge3/etc/profile.d/conda.sh

conda activate obd-py-3

docker-compose up -d
echo "docker-compose up -d" >> /var/log/rmxp.log
