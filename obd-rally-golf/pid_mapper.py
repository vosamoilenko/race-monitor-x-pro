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
from PID.pid_bank1_sensor2_oxygen_sensor_voltage import PIDBank1Sensor2OxygenSensorVoltage
from PID.pid_short_term_fuel_trim_bank1 import PIDShortTermFuelTrimBank1
from PID.pid_fuel_status import PIDFuelStatus
from PID.pid_bank1_sensor1_oxygen_sensor_voltage import PIDBank1Sensor1OxygenSensorVoltage
from PID.pid_oxygen_sensors_present import PIDOxygenSensorsPresent
from PID.pid_commanded_secondary_air_status import PIDCommandedSecondaryAirStatus

class PIDMapper:
    @staticmethod
    def mapHex(hex_string):
        if hex_string is None or hex_string == "NO DATA":
            return None

        command = hex_string[:4]

        if command == '4101':
            return PIDMapper.map(PIDCommand.MONITOR_STATUS, hex_string)
        elif command == '4103':
            return PIDMapper.map(PIDCommand.FUEL_SYSTEM_STATUS, hex_string)
        elif command == '4104':
            return PIDMapper.map(PIDCommand.ENGINE_LOAD, hex_string)
        elif command == '4105':
            return PIDMapper.map(PIDCommand.COOLANT_TEMPERATURE, hex_string)
        elif command == '4106':
            return PIDMapper.map(PIDCommand.SHORT_TERM_FUEL_TRIM_BANK_1, hex_string)
        elif command == '410B':
            return PIDMapper.map(PIDCommand.INTAKE_MANIFOLD_PRESSURE, hex_string)
        elif command == '410C':
            return PIDMapper.map(PIDCommand.ENGINE_SPEED, hex_string)
        elif command == '410D':
            return PIDMapper.map(PIDCommand.VEHICLE_SPEED, hex_string)
        elif command == '410E':
            return PIDMapper.map(PIDCommand.TIMING_ADVANCE, hex_string)
        elif command == '410F':
            return PIDMapper.map(PIDCommand.INTAKE_AIR_TEMPERATURE, hex_string)
        elif command == '4110':
            return PIDMapper.map(PIDCommand.MAF_SENSOR_AIR_FLOW_RATE, hex_string)
        elif command == '4111':
            return PIDMapper.map(PIDCommand.THROTTLE_POSITION, hex_string)
        elif command == '4112':
            return PIDMapper.map(PIDCommand.COMMANDED_SECONDARY_AIR_STATUS, hex_string)
        elif command == '4113':
            return PIDMapper.map(PIDCommand.OXYGEN_SENSORS_PRESENT, hex_string)
        elif command == '4114':
            return PIDMapper.map(PIDCommand.BANK_1_SENSOR_1_OXYGEN_SENSOR_VOLTAGE, hex_string)
        elif command == '4115':
            return PIDMapper.map(PIDCommand.BANK_1_SENSOR_2_OXYGEN_SENSOR_VOLTAGE, hex_string)
        else:
            print(command)
            return "Unknown command"


    @staticmethod
    def map(command, hex_string):
        if hex_string is None or hex_string == "NO DATA":
            return None

        if command == PIDCommand.MONITOR_STATUS:
            return PIDMonitorStatus.parse(hex_string)
        elif command == PIDCommand.FUEL_SYSTEM_STATUS:
            return PIDFuelStatus.parse(hex_string)
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
        elif command == PIDCommand.OXYGEN_SENSORS_PRESENT:
            return PIDBank1Sensor1OxygenSensorVoltage.parse(hex_string)
        elif command == PIDCommand.COMMANDED_SECONDARY_AIR_STATUS:
            return PIDCommandedSecondaryAirStatus.parse(hex_string)
        elif command == PIDCommand.BANK_1_SENSOR_1_OXYGEN_SENSOR_VOLTAGE:
            return PIDBank1Sensor1OxygenSensorVoltage.parse(hex_string)
        elif command == PIDCommand.BANK_1_SENSOR_2_OXYGEN_SENSOR_VOLTAGE:
            return PIDBank1Sensor2OxygenSensorVoltage.parse(hex_string)
        elif command == PIDCommand.SHORT_TERM_FUEL_TRIM_BANK_1:
            return PIDShortTermFuelTrimBank1.parse(hex_string)
        else:
            return "Unknown command"

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
