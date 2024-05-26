import serial
import time

SERIAL_PORT = '/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_8503331323735180F062-if00'

class Arduino:
    def __init__(self):
        try:
            self.ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)
            print("Connected to Arduino.")
        except Exception as e:
            print(f"Failed to connect to Arduino: {e}")

    def listen(self, callback):
        try:
            while True:
                if self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('utf-8').rstrip()
                    print("Arduino says:", line)  # Print whatever is received from the Arduino
                    callback(line)
        except Exception as e:
            print(f"Error reading from Arduino: {e}")

    def send(self, message):
        self.ser.write(message.encode('utf-8'))  # Encode and send message

