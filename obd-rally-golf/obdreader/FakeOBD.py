import random
import time

def random_temp(): return random.randint(-40, 215)  # Temperature in Celsius
def random_pressure(): return random.randint(10, 150)  # Pressure in kPa
def random_voltage(): return round(random.uniform(0, 1.5), 1)  # Voltage in Volts
def random_percent(): return random.randint(0, 100)  # Percentage
def random_ratio(): return round(random.uniform(0, 2), 2)  # Fuel-air equivalence ratio
def random_time_seconds(): return random.randint(0, 3600)  # Time in seconds
def random_rpm(): return random.randint(0, 8000)  # Engine RPM
def random_speed(): return random.randint(0, 240)  # Speed in km/h
def random_flow_rate(): return round(random.uniform(0, 100), 1)  # Flow rate in grams/sec

class FakeOBD:
    def getAllPIDsData(self):
        time.sleep(30)
        return {
            'monitorStatusSinceDtcsCleared': random.choice(['OK', 'NOT OK']),
            'freezeDtc': 'P' + str(random.randint(1000, 1999)),
            'fuelSystemStatus': random.choice(['Open loop', 'Closed loop', 'Open loop due to insufficient temperature', 'Closed loop, but response fault']),
            'calculatedEngineLoad': random_percent(),
            'engineCoolantTemperature': random_temp(),
            'shortTermFuelTrimBank1': random.uniform(-10.0, 10.0),
            'longTermFuelTrimBank1': random.uniform(-10.0, 10.0),
            'shortTermFuelTrimBank2': random.uniform(-10.0, 10.0),
            'longTermFuelTrimBank2': random.uniform(-10.0, 10.0),
            'fuelPressure': random_pressure(),
            'intakeManifoldAbsolutePressure': random_pressure(),
            'engineRpm': random_rpm(),
            'vehicleSpeed': random_speed(),
            'timingAdvance': random.uniform(0.0, 20.0),  # Degrees relative to #1 cylinder
            'intakeAirTemperature': random_temp(),
            'mafAirFlowRate': random_flow_rate(),
            'throttlePosition': random_percent(),
            'commandedSecondaryAirStatus': random.choice(['Pumped', 'Not pumped']),
            'oxygenSensorsPresent': random.randint(0, 8),
            'bank1Sensor1OxygenSensorVoltage': random_voltage(),
            'bank1Sensor2OxygenSensorVoltage': random_voltage(),
            'bank1Sensor3OxygenSensorVoltage': random_voltage(),
            'bank1Sensor4OxygenSensorVoltage': random_voltage(),
            'bank2Sensor1OxygenSensorVoltage': random_voltage(),
            'bank2Sensor2OxygenSensorVoltage': random_voltage(),
            'bank2Sensor3OxygenSensorVoltage': random_voltage(),
            'bank2Sensor4OxygenSensorVoltage': random_voltage(),
            'obdStandardsVehicleConformsTo': random.randint(1, 20),
            'oxygenSensorsPresent2': random.randint(0, 8),
            'auxiliaryInputStatus': random.choice(['Active', 'Inactive']),
            'runTimeSinceEngineStart': random_time_seconds(),
            'distanceTraveledWithMalfunctionIndicatorLampOn': random.randint(0, 10000),  # Distance in km
            'fuelRailPressure': random_pressure(),
            'fuelRailGaugePressure': random_pressure(),
            'oxygenSensor1FuelAirEquivalenceRatio': random_ratio(),
            'oxygenSensor2FuelAirEquivalenceRatio': random_ratio(),
            'oxygenSensor3FuelAirEquivalenceRatio': random_ratio(),
            'oxygenSensor4FuelAirEquivalenceRatio': random_ratio(),
            'oxygenSensor5FuelAirEquivalenceRatio': random_ratio(),
            'oxygenSensor6FuelAirEquivalenceRatio': random_ratio(),
            'oxygenSensor7FuelAirEquivalenceRatio': random_ratio(),
            'oxygenSensor8FuelAirEquivalenceRatio': random_ratio(),
            'catalystTemperatureBank1Sensor1': random_temp(),
            'catalystTemperatureBank1Sensor2': random_temp(),
            'catalystTemperatureBank2Sensor1': random_temp(),
            'catalystTemperatureBank2Sensor2': random_temp(),
            'monitorDriveCycleStatus': random.choice(['Complete', 'Incomplete']),
            'controlModuleVoltage': random.uniform(12.0, 14.5),  # Voltage in Volts
            'absoluteLoadValue': random_percent(),
            'fuelAirCommandedEquivalenceRatio': random_ratio(),
            'relativeThrottlePosition': random_percent(),
            'ambientAirTemperature': random_temp(),
            'absoluteThrottlePositionB': random_percent(),
            'absoluteThrottlePositionC': random_percent(),
            'acceleratorPedalPositionD': random_percent(),
            'acceleratorPedalPositionE': random_percent(),
            'acceleratorPedalPositionF': random_percent(),
            'commandedThrottleActuator': random_percent(),
            'timeRunWithMilOn': random_time_seconds(),
            'timeSinceTroubleCodesCleared': random_time_seconds(),
            'maximumValueForFuelAirEquivalenceRatio': random_ratio(),
            'maximumValueForOxygenSensorVoltage': random_voltage(),
            'maximumValueForOxygenSensorCurrent': random.uniform(0.1, 1.0),  # Current in Amperes
            'maximumValueForIntakeManifoldAbsolutePressure': random_pressure(),
            'maximumValueForAirFlowRateFromMAF': random_flow_rate(),
            'fuelType': random.choice(['Gasoline', 'Diesel', 'Hybrid', 'Electric']),
            'ethanolFuelPercentage': random.uniform(0.0, 100.0),
            'absoluteEvapSystemVaporPressure': random.uniform(0.0, 10.0),  # Pressure in kPa
            'evapSystemVaporPressure': random.uniform(-10.0, 10.0),  # Pressure in kPa
            'shortTermSecondaryOxygenSensorTrimBank1And3': random.uniform(-10.0, 10.0),
            'longTermSecondaryOxygenSensorTrimBank1And3': random.uniform(-10.0, 10.0),
            'shortTermSecondaryOxygenSensorTrimBank2And4': random.uniform(-10.0, 10.0),
            'longTermSecondaryOxygenSensorTrimBank2And4': random.uniform(-10.0, 10.0),
            'fuelRailAbsolutePressure': random_pressure(),
            'relativeAcceleratorPedalPosition': random_percent(),
            'hybridBatteryPackRemainingLife': random_percent(),
            'engineOilTemperature': random_temp(),
            'fuelInjectionTiming': random.uniform(0.0, 30.0),  # Timing in degrees
            'engineFuelRate': random.uniform(0.0, 20.0),  # Fuel rate in liters per hour
            'emissionRequirementsToWhichVehicleIsDesigned': random.choice(['Euro 6', 'Tier 2', 'LEV III']),
            'engineDemandTorquePercentage': random_percent(),
            'actualEngineTorquePercentage': random_percent(),
            'engineReferenceTorque': random.randint(100, 500),  # Torque in Nm
            'enginePercentTorqueData': [random_percent() for _ in range(5)],  # Random percentage list for 5 data points
            'auxiliaryInputOutputSupported': random.choice([True, False]),
            'massAirFlowSensor': random_flow_rate(),
            'engineCoolantTemperature': random_temp(),
            'intakeAirTemperatureSensor': random_temp(),
            'commandedEgrAndEgrError': random.uniform(0.0, 100.0),
            'commandedDieselIntakeAirFlowControlAndRelativeIntakeAirFlowPosition': random_percent(),
            'exhaustGasRecirculationTemperature': random_temp(),
            'commandedThrottleActuatorControlAndRelativeThrottlePosition': random_percent(),
            'fuelPressureControlSystem': random_percent(),
            'injectionPressureControlSystem': random_percent(),
            'turbochargerCompressorInletPressure': random_pressure(),
            'boostPressureControl': random_percent(),
            'variableGeometryTurboControl': random_percent(),
            'wastegateControl': random_percent(),
            'exhaustPressure': random_pressure(),
            'turbochargerRpm': random.randint(0, 100000),
            'turbochargerTemperature': random_temp(),
            'chargeAirCoolerTemperature': random_temp(),
            'exhaustGasTemperature': random_temp(),
            'dieselParticulateFilterPressure': random_pressure(),
            'dieselParticulateFilterTemperature': random_temp(),
            'noxNTEControlAreaStatus': random.choice(['Inside', 'Outside']),
            'pmNTEControlAreaStatus': random.choice(['Inside', 'Outside']),
            'engineRunTime': random_time_seconds(),
            'engineRunTimeForAuxiliaryEmissionsControlDevice1': random_time_seconds(),
            'engineRunTimeForAuxiliaryEmissionsControlDevice2': random_time_seconds(),
            'noxSensor': random_voltage(),  # Assuming voltage as an example value type
            'manifoldSurfaceTemperature': random_temp(),
            'noxReagentSystem': random.choice(['OK', 'Not OK', 'Refill Needed']),
            'particulateMatterSensor': random.choice(['Functional', 'Faulty', 'Replace']),
            'intakeManifoldAbsolutePressure': random_pressure(),
            'driversDemandEnginePercentTorque': random_percent(),
            'actualEnginePercentTorque': random_percent(),
            'engineReferenceTorque': random.randint(100, 1000),  # Torque in Nm
            'enginePercentTorqueData': [random_percent() for _ in range(5)],  # Random percentage list for 5 data points
            'auxiliaryInputOutputSupported': random.choice([True, False]),
            'massAirFlowSensor': random_flow_rate(),
            'engineCoolantTemperature': random_temp(),
            'intakeAirTemperatureSensor': random_temp(),
            'actualEgrCommandedEgrAndEgrError': random.uniform(0.0, 100.0),
            'commandedDieselIntakeAirFlowControlAndRelativeIntakeAirFlowPosition': random_percent(),
            'exhaustGasRecirculationTemperature': random_temp(),
            'commandedThrottleActuatorControlAndRelativeThrottlePosition': random_percent(),
            'fuelPressureControlSystem': random_percent(),
            'injectionPressureControlSystem': random_percent(),
            'turbochargerCompressorInletPressure': random_pressure(),
            'boostPressureControl': random_percent(),
            'variableGeometryTurboControl': random_percent(),
            'wastegateControl': random_percent(),
            'exhaustPressure': random_pressure(),
            'turbochargerRpm': random.randint(0, 100000),
            'turbochargerTemperature': random_temp(),
            'chargeAirCoolerTemperature': random_temp(),
            'exhaustGasTemperatureBank1': random_temp(),
            'exhaustGasTemperatureBank2': random_temp(),
            'dieselParticulateFilterPressure': random_pressure(),
            'dieselParticulateFilterTemperature': random_temp(),
            'noxNteControlAreaStatus': random.choice(['Inside', 'Outside']),
            'pmNteControlAreaStatus': random.choice(['Inside', 'Outside']),
            'engineRunTime': random_time_seconds(),
            'engineRunTimeForAuxiliaryEmissionsControlDevice': random_time_seconds(),
            'noxSensor': random_voltage(),
            'manifoldSurfaceTemperature': random_temp(),
            'noxReagentSystem': random.choice(['OK', 'Not OK', 'Refill Needed']),
            'particulateMatterSensor': random.choice(['Functional', 'Faulty', 'Replace']),
            'intakeManifoldAbsolutePressure': random_pressure(),
            'scrInduceSystem': random.choice(['Operational', 'Needs Service']),
            'runTimeForAecdNumbers11To15': random_time_seconds(),
            'runTimeForAecdNumbers16To20': random_time_seconds(),
            'dieselAftertreatment': random.choice(['OK', 'Not OK']),
            'oxygenSensorWideRange': [random_voltage() for _ in range(4)],  # Example with 4 sensors
            'throttlePositionG': random_percent(),
            'engineFrictionPercentTorque': random_percent(),
            'pmSensorBank1And2': random.choice(['OK', 'Replace']),
            'wwhObdVehicleObdSystemInformation': random.choice(['Type 1', 'Type 2']),
            'fuelSystemControl': random.choice(['Stable', 'Unstable']),
            'wwhObdVehicleObdCountersSupport': random.choice([True, False]),
            'noxWarningAndInducementSystem': random.choice(['Normal', 'Warning', 'Critical']),
            'exhaustGasTemperatureSensor': random_temp(),
            'hybridEvVehicleSystemDataBatteryVoltage': random.uniform(200.0, 400.0),  # Voltage in Volts
            'dieselExhaustFluidSensorData': random_percent(),
            'oxygenSensorData': [random_voltage() for _ in range(4)],
            'engineFuelRate': random.uniform(0.0, 30.0),  # Fuel rate in liters per hour
            'engineExhaustFlowRate': random.uniform(10.0, 300.0),  # Flow rate in liters per second
            'fuelSystemPercentageUse': random_percent(),
            'noxSensorCorrectedData': random.uniform(0.0, 1000.0),  # NOx sensor readings in ppm
            'cylinderFuelRate': random.uniform(0.0, 20.0),  # Fuel rate per cylinder in liters per hour
            'evapSystemVaporPressure': random.uniform(-10.0, 10.0),  # Pressure in kPa
            'transmissionActualGear': random.randint(1, 10),  # Current gear
            'commandedDieselExhaustFluidDosing': random.choice(['High', 'Medium', 'Low']),
            'odometer': random.randint(0, 300000),  # Distance in km
            'noxSensorConcentration': random.uniform(0.0, 800.0),  # NOx concentration in ppm
            'absDisableSwitchState': random.choice(['Enabled', 'Disabled']),
            'fuelLevelInput': random_percent(),  # Fuel level as a percentage
            'exhaustParticulateControlSystemDiagnosticTimeCount': random_time_seconds(),
            'fuelPressureAAndB': random_pressure(),
            'particulateControlDriverInducementSystemStatus': random.choice(['Normal', 'Inducement']),
            'distanceSinceReflashOrModuleReplacement': random.randint(0, 50000),  # Distance in km
            'noxControlDiagnosticAndParticulateControlDiagnosticWarningLampStatus': random.choice(['Off', 'On']),
            'fuelLevelInputAB': random_percent(),  # Fuel level as a percentage for systems with dual tanks
            'exhaustParticulateControlSystemDiagnosticTimeCount': random_time_seconds(),
            'fuelPressureAB': random_pressure(),
        }
