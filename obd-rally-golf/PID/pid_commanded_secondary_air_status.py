# -*- coding: utf-8 -*-
class PIDCommandedSecondaryAirStatus():
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
        status_byte = int(bytes_list[0], 16)

        # Define status based on the byte value
        air_status = {
            0x00: "Off",
            0x01: "Upstream",
            0x02: "Downstream of catalytic converter",
            0x04: "From the outside/atmosphere",
            0x08: "Pump commanded on for diagnostics"
        }

        # Get the description from the dictionary or default to unknown
        air_status_description = air_status.get(status_byte, "Unknown status")

        return air_status_description
