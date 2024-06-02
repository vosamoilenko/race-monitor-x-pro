#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import json
import logging
import os
from dotenv import load_dotenv
from obdreader.OBDReader import OBDReader
from mq.PikaClientProducer import PikaClientProducer


load_dotenv()
FAKE_OBD = os.environ.get("FAKE_OBD")
BASE_PATH = os.environ.get("BASE_PATH")
logging.basicConfig(filename=f"{BASE_PATH}/obd-rally-golf/logs/consumer.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
