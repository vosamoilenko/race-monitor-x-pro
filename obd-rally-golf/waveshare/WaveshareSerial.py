# waveshare/WaveshareSerial.py
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import logging
import time
from utils.SerialDevice import SerialDevice

class WaveshareSerial(SerialDevice):
    def __init__(self, serial_port, baud_rate, power_key):
        super(WaveshareSerial, self).__init__(serial_port, baud_rate)  # Corrected for Python 2.7
        self.power_key = power_key

    def power_on(self):
        logging.info('Powering on the device...')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.power_key, GPIO.OUT)
        GPIO.output(self.power_key, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(self.power_key, GPIO.LOW)
        time.sleep(20)
        self.ser.flushInput()
        logging.info('Device is ready')

    def power_off(self):
        logging.info('Powering off the device...')
        GPIO.output(self.power_key, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(self.power_key, GPIO.LOW)
        time.sleep(18)
        self.ser.close()
        GPIO.cleanup()
        logging.info('Device is powered off')
