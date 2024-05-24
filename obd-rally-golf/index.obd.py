#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import json
import logging
import os
from dotenv import load_dotenv
from obdreader.OBDReader import OBDReader
from mq.PikaClientProducer import PikaClientProducer

logging.basicConfig(filename="/home/pi/Developer/py/obd-rally-golf/logs/obd.log",level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

FAKE_OBD = os.environ.get("FAKE_OBD")

rabbitMq = PikaClientProducer('obd')

obd = OBDReader(FAKE_OBD)
obd.initialize()
obd.scanPIDS()

while True:
    data = obd.getAllPIDsData()
    data['ts'] = int(time.time())
    
    json_data = json.dumps(data)

    logging.info(json_data)
    
    rabbitMq.send(json_data)
