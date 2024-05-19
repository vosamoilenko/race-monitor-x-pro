

class PIDShortTermFuelTrimBank1():
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

        # Calculate Short Term Fuel Trim
        # Convert the first byte from hex to an integer
        # The formula used: (value - 128) * 100 / 128 to convert to percentage
        # where 128 is the neutral value (0% trim)
        short_term_fuel_trim = (int(bytes_list[0], 16) - 128) * 100 / 128

        # print("Short Term Fuel Trim - Bank 1: {:.2f}%".format(short_term_fuel_trim))

        return short_term_fuel_trim
