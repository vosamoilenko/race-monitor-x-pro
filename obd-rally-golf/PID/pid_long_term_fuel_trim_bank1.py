# -*- coding: utf-8 -*-
class PIDLongTermFuelTrimBank1():
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

        # Convert the first byte to an integer
        a_byte = int(bytes_list[0], 16)

        # Calculate the long-term fuel trim using the formula: (A - 128) * 100 / 128
        long_term_fuel_trim = ((a_byte - 128) * 100) / 128.0

        # Optional: Format the output to show two decimal places
        # print("Long Term Fuel Trim (Bank 1): {:.2f}%".format(long_term_fuel_trim))

        return long_term_fuel_trim
