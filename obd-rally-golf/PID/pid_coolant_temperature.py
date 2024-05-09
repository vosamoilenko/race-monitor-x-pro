class PIDCoolantTemperature():
    @staticmethod
    def parse(hex_string):
        if len(hex_string) < 4:
            return None

        code = hex_string[:4]
        value = hex_string[4:]

        # Split the hex string into bytes
        bytes_list = [value[i:i+2] for i in range(0, len(value), 2)]

        # Convert the first byte to temperature in Celsius
        temperature_celsius = int(bytes_list[0], 16) - 40

        print("Coolant Temperature: {}°C".format(temperature_celsius))

        return temperature_celsius
