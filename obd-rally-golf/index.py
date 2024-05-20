#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import time
import json
import logging
from pid_mapper import PIDMapper
from constants import ECU_COMMANDS, ELM_COMMANDS, PIDCommand
from waveshare.waveshare import Waveshare
from obdreader.OBDReader import OBDReader
import sys

# Setup the logging configuration
# logging.basicConfig(filename='logs.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Print the version of Python being used
logging.info("Python version")
logging.info(sys.version)
logging.info("Version info.")
logging.info(sys.version_info)

# Assume OBDReader and decode_obd_response are correctly defined elsewhere
obd = OBDReader()
obd.initialize()

waveshare = Waveshare()
response = waveshare.send_at("ATZ", 1)
print(response)

# obd.scanPIDS()
# data = obd.getAllPIDsData()

# print(json.dumps(data, indent=4))


exit(1)


# wave = Waveshare()
# try: 
#     # wave.check_network_status()
#     # wave.reinitialize_network()
#     # wave.test_udp_connection()
#     wave.send_tcp_data()
# finally:
#     wave.power_down()
#     exit(1)
