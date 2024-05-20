#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import json
import logging
from obdreader.OBDReader import OBDReader
from mq.PikaClientProducer import PikaClientProducer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

rabbitMq = PikaClientProducer('obd')

obd = OBDReader()
obd.initialize()
obd.scanPIDS()

while True:
    data = obd.getAllPIDsData()
    data['ts'] = int(time.time())
    
    json_data = json.dumps(data)
    rabbitMq.send(json_data)
