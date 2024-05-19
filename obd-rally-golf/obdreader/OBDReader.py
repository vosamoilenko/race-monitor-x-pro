# obdreader/OBDReader.py
# -*- coding: utf-8 -*-
import logging
from utils.SerialDevice import SerialDevice
from constants import PID_VARIABLE_MAP
from pid_mapper import PIDMapper

SERIAL_PORT='/dev/serial/by-id/usb-NATIONS_N32G43x_Port_MT005330-if00'
BAUD_RATE=38400

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OBDReader:
    def __init__(self):
        self.serial = SerialDevice(SERIAL_PORT, BAUD_RATE)
        self.allPIDs = []

    def send(self, command, sleep):
        return self.serial.send_at(command, sleep)

    def initialize(self):
        print(self.send("ATD", 0))
        print(self.send("ATZ", 0))
        print(self.send("ATE0", 0))
        print(self.send("ATL0", 0))
        print(self.send("ATS0", 0))
        print(self.send("ATH0", 0))
        print(self.send("ATSP3", 0))

        # Sometimes the first request to '0100' returns bus status instead of PIDs, so we do it twice
        self.send("0100", 3)  # We ignore the first result in case it's just bus status like "BUS INIT...OK"

    def scanPIDS(self):
        self.allPIDs = self.query_pids("0100")

    def getAllPIDsData(self):
        data = {}
        for pid in self.allPIDs:
            # Extract the command part of the PID, which should be the last two characters
            command_suffix = pid[-2:]
            variable_name = PID_VARIABLE_MAP.get(pid, "unknownPid{}".format(command_suffix))

            # Logging PID processing
            print("Processing PID:", pid)
            logging.info("PID {}".format(pid))
            
            # Send the command and log the response
            response = self.send(pid, 0)  # Assuming send command requires full PID command like '0101'
            logging.info("PID RESPONSE {}".format(response))

            # Map the variable name to the response
            data[variable_name] = PIDMapper.mapHex(response)
        
        return data

    
    def query_pids(self, base_pid):
        all_supported_pids = []
        current_base = base_pid
        while True:
            response = self.send(current_base, 3)
            if response[:4] == '4100' or response[:4] == '41' + current_base[2:]:
                available_pids = response[4:]
                logging.info("availablePIDs from {}: {}".format(current_base, available_pids))
                parsed_pids = decode_obd_response(available_pids, current_base)
                logging.info("availablePIDs PARSED from {}: {}".format(current_base, parsed_pids))
                all_supported_pids.extend(parsed_pids)
                
                next_base_hex = hex(int(current_base[2:], 16) + 0x20)[2:].upper()  # Move to the next range
                current_base = '01' + next_base_hex.zfill(2)
            else:
                break
        
        return all_supported_pids



    
def decode_obd_response(data, base_pid):
    if not data:
        logging.error("Input data is empty.")
        return []

    binary_str = ''
    try:
        for hex_digit in data:
            if hex_digit.lower() in '0123456789abcdef':
                binary_str += '{:04b}'.format(int(hex_digit, 16))
            else:
                logging.warning("Invalid hex digit found: %s" % hex_digit)
    except ValueError as e:
        logging.error("Error converting hex to binary: %s" % str(e))
        return []

    supported_pids = []
    base_index = int(base_pid[2:], 16)  # Convert base PID from hex string to integer
    binary_str = binary_str[:32]  # Check the first 32 bits for PIDs from the current base
    for index, bit in enumerate(binary_str):
        if bit == '1':
            pid = base_index + index + 1
            supported_pids.append('01{:02X}'.format(pid))  # Format as hexadecimal with zero-padding

    return supported_pids



