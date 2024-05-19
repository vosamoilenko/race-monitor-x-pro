# -*- coding: utf-8 -*-
class PIDVehicleSpeed():
    @staticmethod
    def parse(hex_string):
        if len(hex_string) < 4:
            return None

        code = hex_string[:4]
        value = hex_string[4:]

        # Split the hex string into bytes
        bytes_list = [value[i:i+2] for i in range(0, 1, 2)]

        # Convert bytes to a single value representing speed in km/h
        speed_kmh = int(''.join(bytes_list), 16)

        print("Vehicle Speed: {} km/h".format(speed_kmh))

        return speed_kmh
