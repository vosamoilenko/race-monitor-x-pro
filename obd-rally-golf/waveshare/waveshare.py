# waveshare/waveshare.py
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import serial
import time
from .WaveshareSerial import WaveshareSerial

class Waveshare:
    def __init__(self):
        self.ser = WaveshareSerial('/dev/ttyS0', 115200, 6)
        self.ser.power_on()

    

    
      