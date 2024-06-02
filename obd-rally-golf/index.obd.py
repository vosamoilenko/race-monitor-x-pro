#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import json
import logging
import os
import signal
from dotenv import load_dotenv
from obdreader.OBDReader import OBDReader
from mq.PikaClientProducer import PikaClientProducer

def handle_timeout(signum, frame):
    logging.error("The process has exceeded the time limit and will be terminated.")
    raise TimeoutError("Process timed out and was terminated")

# Set the signal handler and a 60-second alarm
signal.signal(signal.SIGALRM, handle_timeout)
signal.alarm(90)  # Set the timeout limit to 60 seconds

load_dotenv()
FAKE_OBD = os.environ.get("FAKE_OBD")
BASE_PATH = os.environ.get("BASE_PATH")
logging.basicConfig(filename=f"{BASE_PATH}/obd-rally-golf/logs/obd.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

rabbitMq = PikaClientProducer('obd')

obd = OBDReader(FAKE_OBD)
obd.initialize()
obd.scanPIDS()

try:
    while True:
        data = obd.getAllPIDsData()
        data['ts'] = int(time.time())
        json_data = json.dumps(data)
        
        logging.info(json_data)
        rabbitMq.send(json_data)
except TimeoutError:
    logging.error("Script terminated due to timeout.")
    os._exit(1)  # Forcefully exits the program
finally:
    signal.alarm(0)  # Disable the alarm
