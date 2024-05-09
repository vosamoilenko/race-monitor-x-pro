class PIDMAFSensorAirFlowRate():
    @staticmethod
    def parse(hex_string):
        if len(hex_string) < 4:
            return None

        code = hex_string[:4]
        value = hex_string[4:]

        # Split the hex string into bytes
        bytes_list = [value[i:i+2] for i in range(0, len(value), 2)]

        # Convert bytes to a single value representing MAF sensor air flow rate
        maf_sensor_air_flow_rate = ((int(bytes_list[0], 16) * 256) + int(bytes_list[1], 16)) / 100

        # print("MAF Sensor Air Flow Rate: {} g/s".format(maf_sensor_air_flow_rate))

        return maf_sensor_air_flow_rate
