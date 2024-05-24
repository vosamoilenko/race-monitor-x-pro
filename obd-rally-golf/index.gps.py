#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import json
import logging
import redis
from waveshare.waveshare import Waveshare
from mq.PikaClientProducer import PikaClientProducer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to Redis
redis_host = 'localhost'
redis_port = 6379
r = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)

rabbitMq = PikaClientProducer('gps')

def check_if_paused():
    # This function checks if the GPS collection should be paused
    return r.get('pause_gps') is not None and r.get('pause_gps') == 'true'

def callback(lat, lon):
    data = {'lat': lat, 'lon': lon, 'ts': int(time.time())}
    json_data = json.dumps(data)
    rabbitMq.send(json_data)
    logging.info("GPS data sent: %s", json_data)

waveshare = Waveshare()

try:
    while True:  # Loop to continuously check GPS data if not paused
        if check_if_paused():
            time.sleep(10)
            continue
        
        waveshare.getGPS(callback)
        time.sleep(1)  # Sleep for a short interval to not overload the GPS fetch rate
except Exception as e:
    # General exception for any error that occurs during the GPS data fetching
    logging.error("An error occurred: {}".format( str(e)))

finally: 
    # waveshare.ser.power_off()
    logging.info("GPS module powered off.")
