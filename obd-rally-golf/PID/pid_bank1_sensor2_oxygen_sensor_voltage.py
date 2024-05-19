# -*- coding: utf-8 -*-

class PIDBank1Sensor2OxygenSensorVoltage():
    @staticmethod
    def parse(hex_string):
        if len(hex_string) < 4:
            return None
        
        code = hex_string[:4]
        value = hex_string[4:]

        # Split the hex string into bytes
        bytes_list = [value[i:i+2] for i in range(0, len(value), 2)]

        # Check if we have enough bytes
        if len(bytes_list) < 1:
            return None

        # Calculate voltage from the first byte
        # Each unit represents 0.005V for most O2 sensors
        voltage = int(bytes_list[0], 16) * 0.005

        # print("Bank 1 Sensor 2 Oxygen Sensor Voltage: {:.3f}V".format(voltage))

        return voltage
