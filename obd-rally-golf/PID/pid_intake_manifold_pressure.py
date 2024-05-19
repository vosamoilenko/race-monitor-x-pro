# -*- coding: utf-8 -*-
class PIDIntakeManifoldPressure():
    @staticmethod
    def parse(hex_string):
        if len(hex_string) < 4:
            return None

        code = hex_string[:4]
        value = hex_string[4:]

        # Split the hex string into bytes
        bytes_list = [value[i:i+2] for i in range(0, len(value), 2)]

        # Convert bytes to a single value representing pressure in kPa
        pressure_kpa = int(''.join(bytes_list), 16) / 100

        # print("Intake Manifold Pressure: {} kPa".format(pressure_kpa))

        return pressure_kpa
