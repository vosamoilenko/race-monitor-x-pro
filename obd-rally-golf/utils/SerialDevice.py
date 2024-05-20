# utils/SerialDevice.py
# -*- coding: utf-8 -*-
import logging
import serial
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SerialDevice(object):  # Explicit new-style class
    def __init__(self, serial_port, baud_rate):
        logging.info("Initializing serial connection on {} with baud rate {}".format(serial_port, baud_rate))
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(self.serial_port, baudrate=self.baud_rate, timeout=1)
        self.ser.flushInput()
        logging.info("Serial input flushed and ready.")

    def read_response(self, serial_port):
        response = b''
        start_time = time.time()
        logging.debug("Starting to read the serial response.")
        while time.time() - start_time < serial_port.timeout:
            buffer = serial_port.readline()
            if buffer:
                logging.info("Received buffer: %s", buffer)
                response += buffer
            else:
                logging.debug("No data received in the current loop.")
        if response:
            logging.info("Complete response received: %s", response)
        else:
            logging.warning("No response was compiled from the device.")
        return response.strip()

    def send_at(self, command, sleep):
        logging.info('Preparing to send AT command: %s', command)
        self.ser.write((command + '\r\n').encode())
        logging.debug('AT command sent, waiting for response.')

        time.sleep(sleep)
        
        response = self.read_response(self.ser)

        return response.decode()
