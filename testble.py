import serial
import time

ser = serial.Serial('/dev/rfcomm0', baudrate=38400, timeout=1)
ser.write(b'ATZ\r')  # Reset command
time.sleep(1)  # Give some time to respond
response = ser.read_all()
print(response.decode())
ser.close()
