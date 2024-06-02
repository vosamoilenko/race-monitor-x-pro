#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import json
import os
import logging
from dotenv import load_dotenv
from waveshare.waveshare import Waveshare
from mq.PikaClientProducer import PikaClientProducer

load_dotenv()

BASE_PATH = os.environ.get("BASE_PATH")
FAKE_GPS = os.environ.get("FAKE_GPS")

logging.basicConfig(filename=f"{BASE_PATH}/obd-rally-golf/logs/consumer.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

rabbitMq = PikaClientProducer('gps')

def callback(lat, lon):
    data = {'lat': lat, 'lon': lon, 'ts': int(time.time())}
    json_data = json.dumps(data)
    rabbitMq.send(json_data)
    logging.info("GPS data sent: %s", json_data)

waveshare = Waveshare(FAKE_GPS)

try:
    waveshare.initGPS()
    while True: 
        waveshare.getGPS(callback)
        time.sleep(1)
except Exception as e:
    logging.error("An error occurred: {}".format( str(e)))

finally: 
    waveshare.power_off()
    logging.info("GPS module powered off.")
