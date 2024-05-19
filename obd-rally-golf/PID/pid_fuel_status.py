# -*- coding: utf-8 -*-

class PIDFuelStatus():
    @staticmethod
    def parse(hex_string):
        if len(hex_string) < 4:
            return None

        code = hex_string[:4]
        value = hex_string[4:]

        # Split the hex string into bytes
        bytes_list = [value[i:i+2] for i in range(0, len(value), 2)]

        # Check if we have at least one byte to read
        if len(bytes_list) < 1:
            return None

        # Convert the first byte from hex to an integer
        status_code = int(bytes_list[0], 16)

        # Mapping of common fuel system status codes to their meanings
        status_map = {
            0: "System off (not available)",
            1: "Open loop due to insufficient engine temperature",
            2: "Closed loop, using oxygen sensor feedback to determine fuel mix",
            4: "Open loop due to engine load OR fuel cut due to deceleration",
            8: "Open loop due to system failure",
            16: "Closed loop, but fault with at least one oxygen sensor",
            32: "In use (other)"
        }

        # Fetch the description for the status code
        fuel_status = status_map.get(status_code, "Unknown fuel system status")

        # print("Fuel System Status: {}".format(fuel_status))

        return fuel_status
