# -*- coding: utf-8 -*-
class PIDFuelAirCommandedEquivalenceRatio():
    @staticmethod
    def parse(hex_string):
        if len(hex_string) < 6:
            return None  # Ensure there's enough data for both bytes A and B

        code = hex_string[:4]
        value = hex_string[4:]

        # Split the hex string into bytes
        bytes_list = [value[i:i+2] for i in range(0, len(value), 2)]

        # Check if we have enough bytes
        if len(bytes_list) < 2:
            return None

        # Convert bytes A and B to integers
        byte_a = int(bytes_list[0], 16)
        byte_b = int(bytes_list[1], 16)

        # Calculate the commanded equivalence ratio using the formula: (256*A + B) / 32768
        equivalence_ratio = (256 * byte_a + byte_b) / 32768.0

        # Optional: Format the output to show more precision
        # print("Fuel-Air Commanded Equivalence Ratio: {:.4f}".format(equivalence_ratio))

        return equivalence_ratio
