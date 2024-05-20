#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import json
import logging
from waveshare.waveshare import Waveshare
from mq.PikaClientProducer import PikaClientProducer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

rabbitMq = PikaClientProducer('gps')

def callback(lat, lon):
    data = {'lat': lat, 'lon': lon, 'ts': int(time.time())}

    json_data = json.dumps(data)
    rabbitMq.send(json_data)

waveshare = Waveshare()

try:
    waveshare.getGPS(callback)
finally: 
    waveshare.ser.power_off()


