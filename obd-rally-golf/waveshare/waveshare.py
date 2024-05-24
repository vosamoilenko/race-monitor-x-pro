# waveshare/waveshare.py
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time
import json
import logging
from .WaveshareSerial import WaveshareSerial
from .FakeWaveshare import FakeWaveshare
import subprocess

class Waveshare:
    def __init__(self, isFakeGPS):
        self.isFakeGPS = isFakeGPS == 'true'
        self.fakeWaveshare = FakeWaveshare()

        if self.isFakeGPS:
            return

        self.ser = WaveshareSerial('/dev/ttyS0', 115200, 6)
        
    def initGPS(self):
        if self.isFakeGPS:
            return

        self.ser.send_at('AT+CGPS=1,1', 1)
        time.sleep(1)

    def power_off(self):
        if self.isFakeGPS:
            return
            
        self.ser.power_off()

    def getGPS(self, callback):
        if self.isFakeGPS:
            return self.fakeWaveshare.getGPS(callback)
        
        gps_data = self.ser.send_at('AT+CGPSINFO', 1)
        if gps_data:
            try:
                lat, lon = parse_gps_data(gps_data)
                if lat is not None and lon is not None:
                    logging.info('Latitude: %s, Longitude: %s', lat, lon)
                    callback(lat, lon)
                else:
                    logging.info('Incomplete GPS data, retrying...')
            except Exception as e:
                # General exception for any error that occurs during the GPS data fetching
                logging.error("An error occurred: {}".format( str(e)))
        else:
            logging.info('No GPS data received. Retrying...')

    def sendToFirebase(self, data, access_token):
        project_id = "race-monitor-pro-x"
        document_path = "data/vova"
        url = "https://firestore.googleapis.com/v1/projects/{}/databases/(default)/documents/{}?updateMask.fieldPaths=history".format(project_id, document_path)
        payload = {
            "fields": {
                "history": {
                    "arrayValue": {
                        "values": [
                            data
                        ]
                    }
                }
            }
        }
        payload_json = json.dumps(payload)
        
        print(self.ser.send_at('AT+HTTPTERM', 1))
        print(self.ser.send_at('AT+CSQ', 1))
        print(self.ser.send_at('AT+CREG?', 1))
        print(self.ser.send_at('AT+CGREG?', 1))
        print(self.ser.send_at('AT+CPSI?', 1))

        # Initialize HTTP service
        print(self.ser.send_at('AT+HTTPINIT', 1))
        # print(self.ser.send_at('AT+HTTPPARA="URL","https://firestore.googleapis.com/v1/projects/race-monitor-pro-x/databases/(default)/documents/data?documentId=vova"', 1))
        print(url)
        print(self.ser.send_at('AT+HTTPPARA="URL","{}"'.format(url), 1))
        print(self.ser.send_at('AT+HTTPPARA="CONTENT","application/json"', 1))
        print(self.ser.send_at('AT+HTTPPARA="USERDATA","Authorization: Bearer %s"' % access_token, 1))

        print(self.ser.send_at('AT+HTTPDATA=%d,10000' % len(payload_json), 1))
        print(self.ser.send_at(payload_json, 2))
        

        print(self.ser.send_at('AT+HTTPACTION=2', 1)) #PATCH?
        # print(self.ser.send_at('AT+HTTPACTION=1', 1)) #POST
        # print(self.ser.send_at('AT+HTTPACTION=0', 1)) #GET
        time.sleep(2)
        print(self.ser.send_at('AT+HTTPREAD=0,500', 3))



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

        

    

    
      