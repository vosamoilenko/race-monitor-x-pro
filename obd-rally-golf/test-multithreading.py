import serial
import time
import subprocess
import logging
import RPi.GPIO as GPIO

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Serial port for 4G hat
serial_port = '/dev/ttyS0'
baud_rate = 115200

# GPIO setup
power_key = 6

def send_at(command, back, timeout):
    ser.write((command + '\r\n').encode())
    time.sleep(timeout)
    if ser.inWaiting():
        time.sleep(0.01)
        rec_buff = ser.read(ser.in_waiting).decode()
        logging.debug("Received response: %s", rec_buff)
    else:
        logging.warning('No response received for command: %s', command)
        return None

    if back not in rec_buff:
        logging.error('%s ERROR: %s', command, rec_buff)
        return None
    else:
        return rec_buff

def parse_gps_data(gps_data):
    if not gps_data or '+CGPSINFO: ,,,,,,,' in gps_data:
        logging.info("No valid GPS data available.")
        return None, None

    components = gps_data.split(',')
    
    try:
        # Extract latitude data
        lat_data = components[0].split(':')[1].strip()
        lat_deg = int(lat_data[:2])
        lat_min = float(lat_data[2:])
        lat_dir = components[1].strip()
        
        # Extract longitude data
        lon_data = components[2].strip()
        lon_deg = int(lon_data[:3])
        lon_min = float(lon_data[3:])
        lon_dir = components[3].strip()
        
        # Convert to decimal degrees
        final_lat = lat_deg + (lat_min / 60)
        final_lon = lon_deg + (lon_min / 60)
        
        # Apply direction to the coordinates
        if lat_dir == 'S':
            final_lat = -final_lat
        if lon_dir == 'W':
            final_lon = -final_lon
        
        return final_lat, final_lon
    except ValueError:
        logging.error("Error processing GPS data. Check data format.")
        return None, None

def get_gps_position():
    logging.info('Start GPS session...')
    send_at('AT+CGPS=1,1', 'OK', 1)
    time.sleep(2)

    while True:
        gps_data = send_at('AT+CGPSINFO', '+CGPSINFO:', 1)
        if gps_data:
            lat, lon = parse_gps_data(gps_data)
            if lat is not None and lon is not None:
                logging.info('Latitude: %s, Longitude: %s', lat, lon)
                return lat, lon
            else:
                logging.info('Incomplete GPS data, retrying...')
        else:
            logging.info('No GPS data received. Retrying...')
        time.sleep(1.5)

def power_on():
    logging.info('SIM7600X is starting:')
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(power_key, GPIO.OUT)
    GPIO.output(power_key, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(power_key, GPIO.LOW)
    time.sleep(20)
    ser.flushInput()
    logging.info('SIM7600X is ready')

def power_down():
    logging.info('SIM7600X is logging off:')
    GPIO.output(power_key, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(power_key, GPIO.LOW)
    time.sleep(18)
    ser.close()
    GPIO.cleanup()
    logging.info('Goodbye')

def get_access_token():
    logging.info("Obtaining access token using gcloud")
    try:
        result = subprocess.check_output(['gcloud', 'auth', 'print-access-token'])
        access_token = result.decode('utf-8').strip()
        logging.info("Access token obtained")
        return access_token
    except subprocess.CalledProcessError as e:
        logging.error("Failed to obtain access token: %s", e.output)
        return None

def send_http_request(lat, lon, access_token):
    logging.info("Starting HTTP request")
    http_ser = serial.Serial(serial_port, baudrate=baud_rate, timeout=1)

    # Initialize and configure 4G hat for HTTP
    logging.info("Initializing and configuring 4G hat for HTTP")
    send_at('AT+CFUN=1', 'OK', 1)
    send_at('AT+CGDCONT=1,"IP","your_apn"', 'OK', 1)
    send_at('AT+CGACT=1,1', 'OK', 1)

    # Open GPRS context
    logging.info("Opening GPRS context")
    send_at('AT+SAPBR=3,1,"Contype","GPRS"', 'OK', 1)
    send_at('AT+SAPBR=3,1,"APN","your_apn"', 'OK', 1)
    send_at('AT+SAPBR=1,1', 'OK', 1)
    send_at('AT+SAPBR=2,1', 'OK', 1)

    # Initialize HTTP service
    logging.info("Initializing HTTP service")
    send_at('AT+HTTPINIT', 'OK', 1)
    send_at('AT+HTTPPARA="CID",1', 'OK', 1)
    send_at('AT+HTTPPARA="URL","https://firestore.googleapis.com/v1/projects/race-monitor-pro-x/databases/(default)/documents/data"', 'OK', 1)
    send_at('AT+HTTPPARA="CONTENT","application/json"', 'OK', 1)
    send_at('AT+HTTPPARA="USERDATA","Authorization: Bearer %s"' % access_token, 'OK', 1)

    # Prepare JSON data
    json_data = '{"fields": {"latitude": {"doubleValue": %f}, "longitude": {"doubleValue": %f}}}' % (lat, lon)
    logging.info("Preparing JSON data: %s", json_data)
    send_at('AT+HTTPDATA=%d,10000' % len(json_data), 'DOWNLOAD', 1)
    send_at(json_data, 'OK', 10)

    # Send HTTP POST request
    logging.info("Sending HTTP POST request")
    send_at('AT+HTTPACTION=1', '200', 1)
    response = send_at('AT+HTTPREAD', '', 1)
    logging.info("Received HTTP response: %s", response)

    # Terminate HTTP service and close GPRS context
    logging.info("Terminating HTTP service and closing GPRS context")
    send_at('AT+HTTPTERM', 'OK', 1)
    send_at('AT+SAPBR=0,1', 'OK', 1)

    http_ser.close()
    logging.info("HTTP request finished")

if __name__ == '__main__':
    logging.info("Starting main script")

    ser = serial.Serial(serial_port, baudrate=baud_rate)
    ser.flushInput()

    try:
        power_on()

        # Obtain GPS coordinates
        lat, lon = get_gps_position()
        if lat is not None and lon is not None:
            # Get access token
            access_token = get_access_token()
            if access_token:
                # Send data to Firestore
                send_http_request(lat, lon, access_token)

    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt received, shutting down...")

    
    except Exception as err:
        logging.error("Error: {}".format(err))


    finally:
        power_down()
        logging.info("Main script finished")


# import serial
# import time
# import subprocess
# import logging
# import RPi.GPIO as GPIO

# # Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# # Serial port for 4G hat
# serial_port = '/dev/ttyS0'
# baud_rate = 115200

# # GPIO setup
# power_key = 6

# def send_at(command, back, timeout):
#     ser.write((command + '\r\n').encode())
#     time.sleep(timeout)
#     if ser.inWaiting():
#         time.sleep(0.01)
#         rec_buff = ser.read(ser.inWaiting()).decode()
#         logging.debug("Received response: %s", rec_buff)
#     else:
#         logging.warning('GPS is not ready')
#         return None

#     if back not in rec_buff:
#         logging.error('%s ERROR: %s', command, rec_buff)
#         return None
#     else:
#         return rec_buff

# def parse_gps_data(gps_data):
#     if not gps_data or '+CGPSINFO: ,,,,,,,' in gps_data:
#         logging.info("No valid GPS data available.")
#         return None, None

#     components = gps_data.split(',')
    
#     try:
#         # Extract latitude data
#         lat_data = components[0].split(':')[1].strip()
#         lat_deg = int(lat_data[:2])
#         lat_min = float(lat_data[2:])
#         lat_dir = components[1].strip()
        
#         # Extract longitude data
#         lon_data = components[2].strip()
#         lon_deg = int(lon_data[:3])
#         lon_min = float(lon_data[3:])
#         lon_dir = components[3].strip()
        
#         # Convert to decimal degrees
#         final_lat = lat_deg + (lat_min / 60)
#         final_lon = lon_deg + (lon_min / 60)
        
#         # Apply direction to the coordinates
#         if lat_dir == 'S':
#             final_lat = -final_lat
#         if lon_dir == 'W':
#             final_lon = -final_lon
        
#         return final_lat, final_lon
#     except ValueError:
#         logging.error("Error processing GPS data. Check data format.")
#         return None, None

# def get_gps_position():
#     logging.info('Start GPS session...')
#     send_at('AT+CGPS=1,1', 'OK', 1)
#     time.sleep(2)

#     while True:
#         gps_data = send_at('AT+CGPSINFO', '+CGPSINFO:', 1)
#         if gps_data:
#             lat, lon = parse_gps_data(gps_data)
#             if lat is not None and lon is not None:
#                 logging.info('Latitude: %s, Longitude: %s', lat, lon)
#                 return lat, lon
#             else:
#                 logging.info('Incomplete GPS data, retrying...')
#         else:
#             logging.info('No GPS data received. Retrying...')
#         time.sleep(1.5)

# def power_on():
#     logging.info('SIM7600X is starting:')
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setwarnings(False)
#     GPIO.setup(power_key, GPIO.OUT)
#     GPIO.output(power_key, GPIO.HIGH)
#     time.sleep(2)
#     GPIO.output(power_key, GPIO.LOW)
#     time.sleep(20)
#     ser.flushInput()
#     logging.info('SIM7600X is ready')

# def power_down():
#     logging.info('SIM7600X is logging off:')
#     GPIO.output(power_key, GPIO.HIGH)
#     time.sleep(3)
#     GPIO.output(power_key, GPIO.LOW)
#     time.sleep(18)
#     ser.close()
#     GPIO.cleanup()
#     logging.info('Good bye')

# def get_access_token():
#     logging.info("Obtaining access token using gcloud")
#     try:
#         result = subprocess.check_output(['gcloud', 'auth', 'print-access-token'])
#         access_token = result.decode('utf-8').strip()
#         logging.info("Access token obtained")
#         return access_token
#     except subprocess.CalledProcessError as e:
#         logging.error("Failed to obtain access token: %s", e.output)
#         return None

# def send_http_request(lat, lon, access_token):
#     logging.info("Starting HTTP request thread")
#     http_ser = serial.Serial(serial_port, baudrate=baud_rate, timeout=1)

#     # Initialize and configure 4G hat for HTTP
#     logging.info("Initializing and configuring 4G hat for HTTP")
#     send_at_command(http_ser, 'AT+CFUN=1')
#     send_at_command(http_ser, 'AT+CGDCONT=1,"IP","your_apn"')
#     send_at_command(http_ser, 'AT+CGACT=1,1')

#     # Open GPRS context
#     logging.info("Opening GPRS context")
#     send_at_command(http_ser, 'AT+SAPBR=3,1,"Contype","GPRS"')
#     send_at_command(http_ser, 'AT+SAPBR=3,1,"APN","your_apn"')
#     send_at_command(http_ser, 'AT+SAPBR=1,1')
#     send_at_command(http_ser, 'AT+SAPBR=2,1')

#     # Initialize HTTP service
#     logging.info("Initializing HTTP service")
#     send_at_command(http_ser, 'AT+HTTPINIT')
#     send_at_command(http_ser, 'AT+HTTPPARA="CID",1')
#     send_at_command(http_ser, 'AT+HTTPPARA="URL","https://firestore.googleapis.com/v1/projects/race-monitor-pro-x/databases/(default)/documents/data"')
#     send_at_command(http_ser, 'AT+HTTPPARA="CONTENT","application/json"')
#     send_at_command(http_ser, 'AT+HTTPPARA="USERDATA","Authorization: Bearer %s"' % access_token)

#     # Prepare JSON data
#     json_data = '{"fields": {"latitude": {"doubleValue": %f}, "longitude": {"doubleValue": %f}}}' % (lat, lon)
#     logging.info("Preparing JSON data: %s", json_data)
#     send_at_command(http_ser, 'AT+HTTPDATA=%d,10000' % len(json_data))
#     send_at_command(http_ser, json_data, delay=10)

#     # Send HTTP POST request
#     logging.info("Sending HTTP POST request")
#     send_at_command(http_ser, 'AT+HTTPACTION=1')
#     response = send_at_command(http_ser, 'AT+HTTPREAD')
#     logging.info("Received HTTP response: %s", response)

#     # Terminate HTTP service and close GPRS context
#     logging.info("Terminating HTTP service and closing GPRS context")
#     send_at_command(http_ser, 'AT+HTTPTERM')
#     send_at_command(http_ser, 'AT+SAPBR=0,1')

#     http_ser.close()
#     logging.info("HTTP request thread finished")

# if __name__ == '__main__':
#     logging.info("Starting main script")

#     ser = serial.Serial(serial_port, baudrate=baud_rate)
#     ser.flushInput()

#     try:
#         power_on()

#         # Obtain GPS coordinates
#         lat, lon = get_gps_position()
#         if lat is not None and lon is not None:
#             # Get access token
#             access_token = get_access_token()
#             if access_token:
#                 time.sleep(5)
#                 # Send data to Firestore
#                 send_http_request(lat, lon, access_token)

#     except KeyboardInterrupt:
#         logging.info("KeyboardInterrupt received, shutting down...")

#     except Exception as err:
#         logging.error("Error: {}".format(err))

#     finally:
#         power_down()
#         logging.info("Main script finished")
