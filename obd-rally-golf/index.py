#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import time
import logging
from pid_mapper import PIDMapper
from constants import ECU_COMMANDS, ELM_COMMANDS, PIDCommand
from waveshare.waveshare import Waveshare

import sys

# Setup the logging configuration
logging.basicConfig(filename='logs.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Print the version of Python being used
logging.info("Python version")
logging.info(sys.version)
logging.info("Version info.")
logging.info(sys.version_info)

wave = Waveshare()
try: 
    # wave.check_network_status()
    # wave.reinitialize_network()
    # wave.test_udp_connection()
    wave.send_tcp_data()
finally:
    wave.power_down()
    exit(1)

def read_response(serial_port):
    response = b''
    start_time = time.time()
    while time.time() - start_time < serial_port.timeout:
        buffer = serial_port.readline()
        if buffer:
            logging.info("Received buffer: {}".format(buffer))
            response += buffer
    if response:
        logging.info("Complete response received: {}".format(response))
    return response.strip()

def execute_command(serial_port, command):
    try:
        full_command = command['command']
        logging.info("Sending command: {}".format(full_command))
        serial_port.write(full_command.encode())  # Ensure data is correctly encoded
        time.sleep(0.5)
        response = read_response(serial_port)
        decoded_response = response.decode('utf-8')
        logging.info("Decoded response: {}".format(decoded_response))
        return decoded_response
    except serial.SerialException as e:
        error_message = "Serial exception: {}".format(str(e))
        logging.error(error_message)
        return error_message

def execute_ecu_commands(serial_port, commands):
    try:
        with open("ecu_commands_output.txt", "a") as f:
            while True:
                for cmd in commands:
                    command_name = cmd['command']
                    logging.info("\nExecuting command for: {}".format(command_name))
                    try:
                        timestamp = time.time()
                        response = execute_command(serial_port, cmd)
                        f.write("Timestamp: {}\n".format(timestamp))
                        f.write("Command: {}\n".format(command_name))
                        f.write("Response: {}\n".format(response))
                    except Exception as e:
                        logging.error("An error occurred for command {}: {}".format(command_name, e))
                time.sleep(1)  # Execute the commands every second
    except KeyboardInterrupt:
        logging.info("\nProcess interrupted by user.")
    except Exception as e:
        logging.error("An error occurred: {}".format(e))

def execute_commands(serial_port, commands):
    results = []
    for cmd in commands:
        logging.info("\nExecuting command for: {}".format(cmd['description']))
        response = execute_command(serial_port, cmd)
        results.append((cmd['description'], response))
    return results

# Setup the serial connection
logging.info("Initializing serial connection...")
serial_port = serial.Serial('/dev/ttyACM0', 38400, timeout=7)

# Execute ELM and ECU commands
elm_results = execute_commands(serial_port, ELM_COMMANDS)

serial_port.timeout = 1
elm_results = execute_commands(serial_port, ECU_COMMANDS)

wave.send_tcp_data()

print("\nELM327 Responses:")
print("\nECU Responses:")

logging.info("Closing serial connection with obd...")
serial_port.close()

logging.info("Closing serial connection with waveshark...")
wave.power_down()
