#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import serial
import time

ser = serial.Serial("/dev/ttyACM0", 38400, timeout=5)
ser.flushInput()

power_key = 6
rec_buff = ''

try:
    while True:
        command_input = raw_input('Please input the AT command:')
        print('writing to serial')
        ser.write((command_input + '\r\n').encode())
        print("wrote to serial")
        
        time.sleep(0.1)
        print("is inWaiting {}".format(ser.inWaiting()))
        if ser.inWaiting():
            time.sleep(0.01)
            rec_buff = ser.read(ser.inWaiting())
        if rec_buff != '':
            try:
                # Decode using UTF-8 and replace errors
                print(rec_buff.decode('utf-8', 'replace'))
            except UnicodeDecodeError as e:
                print("Decoding error: {}".format(e))
            rec_buff = ''
except Exception as e:
    print('An error occurred: {}'.format(e))
finally:
    ser.close()
