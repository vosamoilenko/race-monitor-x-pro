class PIDIntakeAirTemperature():
    @staticmethod
    def parse(hex_string):
        if len(hex_string) < 4:
            return None

        code = hex_string[:4]
        value = hex_string[4:]

        # Split the hex string into bytes
        bytes_list = [value[i:i+2] for i in range(0, len(value), 2)]

        # Convert byte to a single value representing intake air temperature in Celsius
        intake_air_temp_celsius = int(bytes_list[0], 16) - 40

        # print("Intake Air Temperature: {} °C".format(intake_air_temp_celsius))

        return intake_air_temp_celsius
