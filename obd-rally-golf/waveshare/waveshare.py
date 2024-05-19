#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import serial
import time

class Waveshare:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyS0', 115200)
        self.ser.flushInput()
        self.power_key = 6
        self.APN = 'CMNET'
        self.ServerIP = '66.241.124.119'  # echo.websocket.org
        self.Port = '80'  # HTTP port
        self.setup_modem()

    def power_on(self):
        print('SIM7600X is starting:')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.power_key, GPIO.OUT)
        GPIO.output(self.power_key, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(self.power_key, GPIO.LOW)
        time.sleep(20)
        print('SIM7600X is ready')

    def power_down(self):
        print('SIM7600X is logging off:')
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.power_key, GPIO.OUT)
            GPIO.output(self.power_key, GPIO.HIGH)
            time.sleep(3)
            GPIO.output(self.power_key, GPIO.LOW)
            time.sleep(18)
        finally:
            self.ser.close()
            GPIO.cleanup()
        print('Good bye')

    def send_at(self, command, back, timeout):
        print("Sending AT command: {}".format(command))
        self.ser.write((command + '\r\n').encode())
        time.sleep(timeout)
        rec_buff = ''
        if self.ser.inWaiting():
            time.sleep(0.1)
            rec_buff = self.ser.read(self.ser.inWaiting()).decode()
        if back not in rec_buff:
            print("{} ERROR".format(command))
            print("{} back:\t{}".format(command, rec_buff))
            return None
        else:
            print("Response for {}: {}".format(command, rec_buff))
            return rec_buff

    def setup_modem(self):
        self.power_on()
        print("Setting APN...")
        self.send_at('AT+CGDCONT=1,"IP","{}"'.format(self.APN), 'OK', 2)
        print("Opening network...")
        self.send_at('AT+NETOPEN', '+NETOPEN: 0', 5)
        ip_response = self.send_at('AT+IPADDR', '+IPADDR:', 2)
        print("IP response: {}".format(ip_response))
        # self.send_tcp_request()

    def test_udp_connection(self):
        print("Attempting UDP connection...")
        response = self.send_at('AT+CIPSTART="UDP","echo.websocket.org","80"', 'CONNECT OK', 10)
        if response:
            print('UDP connection attempt successful!')
        else:
            print('UDP connection failed:', response)

    def send_tcp_request(self):
        print("Attempting TCP connection...")
        response = self.send_at('AT+CIPSTART="TCP","{}","{}"'.format(self.ServerIP, self.Port), 'CONNECT OK', 10)
        if response:
            http_get_request = 'GET / HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n'.format(self.ServerIP)
            print("Sending HTTP GET request...")
            self.send_at('AT+CIPSEND', '>', 2)
            self.ser.write(http_get_request.encode())
            if self.send_at('\x1A', 'SEND OK', 5):  # Send Ctrl+Z to signal end of data
                print('Message sent successfully!')
            else:
                print('Failed to send HTTP request.')
        else:
            print('TCP connection failed:', response)
        self.power_down()

    def check_network_status(self):
        print("Checking network status...")
        response = self.send_at('AT+CSQ', 'OK', 2)
        print("Signal quality response: {}".format(response))
        response = self.send_at('AT+CREG?', '+CREG: 0,1', 2)
        print("Network registration response: {}".format(response))
        response = self.send_at('AT+CGREG?', '+CGREG: 0,1', 2)
        print("GPRS network registration response: {}".format(response))

    def reinitialize_network(self):
        print("Reinitializing network connection...")
        self.send_at('AT+NETCLOSE', 'OK', 5)
        self.send_at('AT+NETOPEN', 'OK', 5)
        response = self.send_at('AT+IPADDR', 'OK', 2)
        print("Reinitialized IP address: {}".format(response))



# #!/usr/bin/python
# # -*- coding:utf-8 -*-
# import RPi.GPIO as GPIO
# import serial
# import time
# import threading

# class Waveshare:
#     def __init__(self):
#         self.ser = serial.Serial('/dev/ttyS0', 115200)
#         self.ser.flushInput()
#         self.power_key = 6
#         self.APN = 'CMNET'
#         self.ServerIP = '142.251.37.110'
#         self.Port = '2317'
#         self.positions = []
#         self.keep_running = True

#         # Start GPS polling in a separate thread
#         # self.gps_thread = threading.Thread(target=self.poll_gps)
#         # self.gps_thread.daemon = True
#         # self.gps_thread.start()

#         # Initialize the modem on the main thread
#         self.setup_modem()

#     def setup_modem(self):
#         # try:
#         self.power_on()
#         self.init_modem()
#         # finally:
#         #     self.power_down()

#     def power_on(self):
#         print('SIM7600X is starting:')
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setwarnings(False)
#         GPIO.setup(self.power_key, GPIO.OUT)
#         GPIO.output(self.power_key, GPIO.HIGH)
#         time.sleep(2)
#         GPIO.output(self.power_key, GPIO.LOW)
#         time.sleep(20)
#         print('SIM7600X is ready')

#     def power_down(self):
#         print('SIM7600X is logging off:')
#         GPIO.output(self.power_key, GPIO.HIGH)
#         time.sleep(3)
#         GPIO.output(self.power_key, GPIO.LOW)
#         time.sleep(18)
#         self.ser.close()
#         GPIO.cleanup()
#         print('Good bye')

#     def send_at(self, command, back, timeout):
#         self.ser.write((command + '\r\n').encode())
#         time.sleep(timeout)
#         rec_buff = ''
#         if self.ser.inWaiting():
#             time.sleep(0.1)
#             rec_buff = self.ser.read(self.ser.inWaiting()).decode()
#         if back not in rec_buff:
#             print(command + ' ERROR')
#             print(command + ' back:\t' + rec_buff)
#             return None
#         else:
#             print(rec_buff)
#             return rec_buff

#     def init_modem(self):
#         self.send_at('AT+CGSOCKCONT=1,\"IP\",\"' + self.APN + '\"', 'OK', 1)

#     def send_tcp_data(self):
#         self.send_at('AT+CIPSTART=\"TCP\",\"' + self.ServerIP + '\",\"' + self.Port + '\"', 'CONNECT OK', 10)
#         self.send_at('AT+CIPSEND', '>', 2)
#         self.ser.write(self.Message.encode())
#         if self.send_at('\x1A', 'SEND OK', 5):
#             print('Message sent successfully!')

#     def poll_gps(self):
#         self.send_at('AT+CGPS=1,1', 'OK', 1)
#         while self.keep_running:
#             gps_data = self.send_at('AT+CGPSINFO', '+CGPSINFO:', 1)
#             if gps_data:
#                 lat, lon = self.parse_gps_data(gps_data)
#                 if lat is not None and lon is not None:
#                     self.positions.append((lat, lon))
#                     print('Latitude:', lat, 'Longitude:', lon)
#             time.sleep(5)  # Adjust the sleep time as necessary

#     def parse_gps_data(self, gps_data):
#         # Dummy parser function: Needs real implementation
#         return (0, 0)  # Return dummy latitude and longitude

# # Example usage
# # device = Waveshare()

# # To send data on demand:
# # device.send_tcp_data()
