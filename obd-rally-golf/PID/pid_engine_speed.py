class PIDEngineSpeed():
    @staticmethod
    def parse(hex_string):
        if len(hex_string) < 4:
            return None

        code = hex_string[:4]
        value = hex_string[4:]

        byts = [value[i:i+2] for i in range(0, len(value), 2)]
        rpm = (int(byts[0], 16) * 256 + int(byts[1], 16)) // 4

        # print("RPM: {}".format(rpm))

        return rpm
