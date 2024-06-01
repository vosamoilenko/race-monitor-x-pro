# -*- coding: utf-8 -*-
class PIDBank1Sensor1OxygenSensorVoltage():
    @staticmethod
    def parse(hex_string):
        if len(hex_string) < 4:
            return None

        code = hex_string[:4]
        value = hex_string[4:]

        # Split the hex string into bytes
        bytes_list = [value[i:i+2] for i in range(0, len(value), 2)]

        # Check if we have enough data
        if len(bytes_list) < 2:
            return None

        # Convert bytes to a single value representing Oxygen Sensor Voltage
        # The formula for the voltage is (A * 256 + B) / 2000 volts
        oxygen_sensor_voltage = ((int(bytes_list[0], 16) * 256) + int(bytes_list[1], 16)) / 2000.0

        # print("Oxygen Sensor Voltage: {:.3f} V".format(oxygen_sensor_voltage))

        return oxygen_sensor_voltage
