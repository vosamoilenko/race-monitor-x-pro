# -*- coding: utf-8 -*-
class PIDOxygenSensorsPresent():
    @staticmethod
    def parse(hex_string):
        if len(hex_string) < 4:
            return None

        code = hex_string[:4]
        value = hex_string[4:]

        # Split the hex string into bytes
        bytes_list = [value[i:i+2] for i in range(0, len(value), 2)]

        # Check if we have enough data
        if len(bytes_list) < 1:
            return None

        # Convert the first byte into binary format to check sensor presence
        # Each bit of the byte represents the presence of a sensor, from the least significant bit
        sensors_present = format(int(bytes_list[0], 16), '08b')
        
        # Create a dictionary to map sensor positions to their presence
        sensor_presence = {
            "Sensor 1 (Bank 1)": 'Present' if sensors_present[7] == '1' else 'Not present',
            "Sensor 2 (Bank 1)": 'Present' if sensors_present[6] == '1' else 'Not present',
            "Sensor 3 (Bank 1)": 'Present' if sensors_present[5] == '1' else 'Not present',
            "Sensor 4 (Bank 1)": 'Present' if sensors_present[4] == '1' else 'Not present',
            "Sensor 1 (Bank 2)": 'Present' if sensors_present[3] == '1' else 'Not present',
            "Sensor 2 (Bank 2)": 'Present' if sensors_present[2] == '1' else 'Not present',
            "Sensor 3 (Bank 2)": 'Present' if sensors_present[1] == '1' else 'Not present',
            "Sensor 4 (Bank 2)": 'Present' if sensors_present[0] == '1' else 'Not present'
        }

        return sensor_presence
