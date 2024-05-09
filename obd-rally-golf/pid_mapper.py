from constants import PIDCommand
from PID.pid_engine_speed import PIDEngineSpeed
from PID.pid_monitor_status import PIDMonitorStatus
from PID.pid_engine_load import PIDEngineLoad
from PID.pid_coolant_temperature import PIDCoolantTemperature
from PID.pid_intake_manifold_pressure import PIDIntakeManifoldPressure
from PID.pid_vehicle_speed import PIDVehicleSpeed
from PID.pid_timing_advance import PIDTimingAdvance
from PID.pid_intake_air_temperature import PIDIntakeAirTemperature
from PID.pid_maf_sensor_air_flow_rate import PIDMAFSensorAirFlowRate
from PID.pid_throttle_position import PIDThrottlePosition

class PIDMapper:

    @staticmethod
    def map(command, hex_string):
        if hex_string is None or hex_string == "NO DATA":
            return None

        if command == PIDCommand.MONITOR_STATUS:
            return PIDMonitorStatus.parse(hex_string)
        elif command == PIDCommand.FUEL_SYSTEM_STATUS:
            return PIDMapper.mapFuelSystemStatus(hex_string)
        elif command == PIDCommand.ENGINE_LOAD:
            return PIDEngineLoad.parse(hex_string)
        elif command == PIDCommand.COOLANT_TEMPERATURE:
            return PIDCoolantTemperature.parse(hex_string)
        elif command == PIDCommand.INTAKE_MANIFOLD_PRESSURE:
            return PIDIntakeManifoldPressure.parse(hex_string)
        elif command == PIDCommand.ENGINE_SPEED:
            return PIDEngineSpeed.parse(hex_string)
        elif command == PIDCommand.VEHICLE_SPEED:
            return PIDVehicleSpeed.parse(hex_string)
        elif command == PIDCommand.TIMING_ADVANCE:
            return PIDTimingAdvance.parse(hex_string)
        elif command == PIDCommand.INTAKE_AIR_TEMPERATURE:
            return PIDIntakeAirTemperature.parse(hex_string)
        elif command == PIDCommand.MAF_SENSOR_AIR_FLOW_RATE:
            return PIDMAFSensorAirFlowRate.parse(hex_string)
        elif command == PIDCommand.THROTTLE_POSITION:
            return PIDThrottlePosition.parse(hex_string)
        else:
            return "Unknown command"

    @staticmethod
    def mapFuelSystemStatus(hex_string):
        pass

    @staticmethod
    def mapEngineLoad(hex_string):
        pass

    @staticmethod
    def mapCoolantTemperature(hex_string):
        pass

    @staticmethod
    def mapIntakeManifoldPressure(hex_string):
        pass

    @staticmethod
    def mapEngineSpeed(hex_string):
        if len(hex_string) < 4:
            return None

        code = hex_string[:4]
        value = hex_string[4:]

        byts = [value[i:i+2] for i in range(0, len(value), 2)]
        rpm = (int(byts[0], 16) * 256 + int(byts[1], 16)) // 4

        print("RPM: {}".format(rpm))

        return rpm

    @staticmethod
    def mapVehicleSpeed(hex_string):
         pass

    @staticmethod
    def mapTimingAdvance(hex_string):
        pass

    @staticmethod
    def mapIntakeAirTemperature(hex_string):
        pass

    @staticmethod
    def mapMAFSensorAirFlowRate(hex_string):
        pass

    @staticmethod
    def mapThrottlePosition(hex_string):
        pass



# # Example usage:
# command = PIDCommand.ENGINE_COOLANT_TEMPERATURE
# hex_value = "410A"
# result = PIDMapper.map_pid(command, hex_value)
# print(result)  # Output will depend on the conversion logic for engine coolant temperature
