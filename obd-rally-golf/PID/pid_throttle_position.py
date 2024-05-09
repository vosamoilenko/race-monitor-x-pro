class PIDThrottlePosition():
    @staticmethod
    def parse(hex_string):
        if len(hex_string) < 4:
            return None

        code = hex_string[:4]
        value = hex_string[4:]

        # Split the hex string into bytes
        bytes_list = [value[i:i+2] for i in range(0, len(value), 2)]

        # Convert bytes to throttle position percentage
        throttle_position = (int(bytes_list[0], 16) * 100) / 255

        # print("Throttle Position: {} %".format(throttle_position))

        return throttle_position
