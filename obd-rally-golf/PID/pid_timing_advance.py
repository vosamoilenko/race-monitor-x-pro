# -*- coding: utf-8 -*-
class PIDTimingAdvance():
    @staticmethod
    def parse(hex_string):
        if len(hex_string) < 4:
            return None

        code = hex_string[:4]
        value = hex_string[4:]

        # Split the hex string into bytes
        bytes_list = [value[i:i+2] for i in range(0, len(value), 2)]

        # Convert byte to a single value representing timing advance in degrees
        timing_advance_degrees = int(bytes_list[0], 16) / 2 - 64

        # print("Timing Advance: {} degrees".format(timing_advance_degrees))

        return timing_advance_degrees
