# -*- coding: utf-8 -*-

import serial
import time

pids = [
    # {"command": b'0100\r\n', "dec": 0, "bytes": 4, "description": "PIDs supported [$01 - $20]"},
    # {"command": b'0101\r\n', "dec": 1, "bytes": 4, "description": "Monitor status since DTCs cleared. (Includes malfunction indicator lamp (MIL), status and number of DTCs, components tests, DTC readiness checks)"},
    # {"command": b'0102\r\n', "dec": 2, "bytes": 2, "description": "DTC that caused freeze frame to be stored."},
    {"command": b'0103\r\n', "dec": 3, "bytes": 2, "description": "Fuel system status"},
    {"command": b'0104\r\n', "dec": 4, "bytes": 1, "description": "Calculated engine load"},
    {"command": b'0105\r\n', "dec": 5, "bytes": 1, "description": "Engine coolant temperature"},
    # {"command": b'0106\r\n', "dec": 6, "bytes": 1, "description": "Short term fuel trim (STFT)—Bank 1"},
    # {"command": b'0107\r\n', "dec": 7, "bytes": 1, "description": "Long term fuel trim (LTFT)—Bank 1"},
    # {"command": b'0108\r\n', "dec": 8, "bytes": 1, "description": "Short term fuel trim (STFT)—Bank 2"},
    # {"command": b'0109\r\n', "dec": 9, "bytes": 1, "description": "Long term fuel trim (LTFT)—Bank 2"},
    # {"command": b'010A\r\n', "dec": 10, "bytes": 1, "description": "Fuel pressure (gauge pressure)"},
    {"command": b'010B\r\n', "dec": 11, "bytes": 1, "description": "Intake manifold absolute pressure"},
    {"command": b'010C\r\n', "dec": 12, "bytes": 2, "description": "Engine speed"},
    {"command": b'010D\r\n', "dec": 13, "bytes": 1, "description": "Vehicle speed"},
    {"command": b'010E\r\n', "dec": 14, "bytes": 1, "description": "Timing advance"},
    {"command": b'010F\r\n', "dec": 15, "bytes": 1, "description": "Intake air temperature"},
    {"command": b'0110\r\n', "dec": 16, "bytes": 2, "description": "Mass air flow sensor (MAF) air flow rate"},
    {"command": b'0111\r\n', "dec": 17, "bytes": 1, "description": "Throttle position"},
    # {"command": b'0112\r\n', "dec": 18, "bytes": 1, "description": "Commanded secondary air status"},
    # {"command": b'0113\r\n', "dec": 19, "bytes": 1, "description": "Oxygen sensors present (in 2 banks)"},
    # {"command": b'0114\r\n', "dec": 20, "bytes": 2, "description": "Oxygen Sensor 1, A: Voltage, B: Short term fuel trim"},
    # {"command": b'0115\r\n', "dec": 21, "bytes": 2, "description": "Oxygen Sensor 2, A: Voltage, B: Short term fuel trim"},
    # {"command": b'0116\r\n', "dec": 22, "bytes": 2, "description": "Oxygen Sensor 3, A: Voltage, B: Short term fuel trim"},
    # {"command": b'0117\r\n', "dec": 23, "bytes": 2, "description": "Oxygen Sensor 4, A: Voltage, B: Short term fuel trim"},
    # {"command": b'0118\r\n', "dec": 24, "bytes": 2, "description": "Oxygen Sensor 5, A: Voltage, B: Short term fuel trim"},
    # {"command": b'0119\r\n', "dec": 25, "bytes": 2, "description": "Oxygen Sensor 6, A: Voltage, B: Short term fuel trim"},
    # {"command": b'011A\r\n', "dec": 26, "bytes": 2, "description": "Oxygen Sensor 7, A: Voltage, B: Short term fuel trim"},
    # {"command": b'011B\r\n', "dec": 27, "bytes": 2, "description": "Oxygen Sensor 8, A: Voltage, B: Short term fuel trim"},
    # {"command": b'011C\r\n', "dec": 28, "bytes": 1, "description": "OBD standards this vehicle conforms to"},
    # {"command": b'011D\r\n', "dec": 29, "bytes": 1, "description": "Oxygen sensors present (in 4 banks)"},
    # {"command": b'011E\r\n', "dec": 30, "bytes": 1, "description": "Auxiliary input status"},
    # {"command": b'011F\r\n', "dec": 31, "bytes": 2, "description": "Run time since engine start"},
    # {"command": b'0120\r\n', "dec": 32, "bytes": 4, "description": "PIDs supported [$21 - $40]"},
    # {"command": b'0121\r\n', "dec": 33, "bytes": 2, "description": "Distance traveled with malfunction indicator lamp (MIL) on"},
    # {"command": b'0122\r\n', "dec": 34, "bytes": 2, "description": "Fuel Rail Pressure (relative to manifold vacuum)"},
    # {"command": b'0123\r\n', "dec": 35, "bytes": 2, "description": "Fuel Rail Gauge Pressure (diesel, or gasoline direct injection)"},
    # {"command": b'0124\r\n', "dec": 36, "bytes": 4, "description": "Oxygen Sensor 1 (Air-Fuel Equivalence Ratio, Voltage)"},
    # {"command": b'0125\r\n', "dec": 37, "bytes": 4, "description": "Oxygen Sensor 2 (Air-Fuel Equivalence Ratio, Voltage)"},
    # {"command": b'0126\r\n', "dec": 38, "bytes": 4, "description": "Oxygen Sensor 3 (Air-Fuel Equivalence Ratio, Voltage)"},
    # {"command": b'0127\r\n', "dec": 39, "bytes": 4, "description": "Oxygen Sensor 4 (Air-Fuel Equivalence Ratio, Voltage)"},
    # {"command": b'0128\r\n', "dec": 40, "bytes": 4, "description": "Oxygen Sensor 5 (Air-Fuel Equivalence Ratio, Voltage)"},
    # {"command": b'0129\r\n', "dec": 41, "bytes": 4, "description": "Oxygen Sensor 6 (Air-Fuel Equivalence Ratio, Voltage)"},
    # {"command": b'012A\r\n', "dec": 42, "bytes": 4, "description": "Oxygen Sensor 7 (Air-Fuel Equivalence Ratio, Voltage)"},
    # {"command": b'012B\r\n', "dec": 43, "bytes": 4, "description": "Oxygen Sensor 8 (Air-Fuel Equivalence Ratio, Voltage)"},
    # {"command": b'012C\r\n', "dec": 44, "bytes": 1, "description": "Commanded EGR"},
    # {"command": b'012D\r\n', "dec": 45, "bytes": 1, "description": "EGR Error"},
    # {"command": b'012E\r\n', "dec": 46, "bytes": 1, "description": "Commanded evaporative purge"},
    # {"command": b'012F\r\n', "dec": 47, "bytes": 1, "description": "Fuel Tank Level Input"},
    # {"command": b'0130\r\n', "dec": 48, "bytes": 1, "description": "Warm-ups since codes cleared"},
    # {"command": b'0131\r\n', "dec": 49, "bytes": 2, "description": "Distance traveled since codes cleared"},
    # {"command": b'0132\r\n', "dec": 50, "bytes": 2, "description": "Evap. System Vapor Pressure"},
    # {"command": b'0133\r\n', "dec": 51, "bytes": 1, "description": "Absolute Barometric Pressure"},
    # {"command": b'0134\r\n', "dec": 52, "bytes": 4, "description": "Oxygen Sensor 1 (Air-Fuel Equivalence Ratio, Current)"},
    # {"command": b'0135\r\n', "dec": 53, "bytes": 4, "description": "Oxygen Sensor 2 (Air-Fuel Equivalence Ratio, Current)"},
    # {"command": b'0136\r\n', "dec": 54, "bytes": 4, "description": "Oxygen Sensor 3 (Air-Fuel Equivalence Ratio, Current)"},
    # {"command": b'0137\r\n', "dec": 55, "bytes": 4, "description": "Oxygen Sensor 4 (Air-Fuel Equivalence Ratio, Current)"},
    # {"command": b'0138\r\n', "dec": 56, "bytes": 4, "description": "Oxygen Sensor 5 (Air-Fuel Equivalence Ratio, Current)"},
    # {"command": b'0139\r\n', "dec": 57, "bytes": 4, "description": "Oxygen Sensor 6 (Air-Fuel Equivalence Ratio, Current)"},
    # {"command": b'013A\r\n', "dec": 58, "bytes": 4, "description": "Oxygen Sensor 7 (Air-Fuel Equivalence Ratio, Current)"},
    # {"command": b'013B\r\n', "dec": 59, "bytes": 4, "description": "Oxygen Sensor 8 (Air-Fuel Equivalence Ratio, Current)"},
    # {"command": b'013C\r\n', "dec": 60, "bytes": 2, "description": "Catalyst Temperature: Bank 1, Sensor 1"},
    # {"command": b'013D\r\n', "dec": 61, "bytes": 2, "description": "Catalyst Temperature: Bank 2, Sensor 1"},
    # {"command": b'013E\r\n', "dec": 62, "bytes": 2, "description": "Catalyst Temperature: Bank 1, Sensor 2"},
    # {"command": b'013F\r\n', "dec": 63, "bytes": 2, "description": "Catalyst Temperature: Bank 2, Sensor 2"},
    # {"command": b'0140\r\n', "dec": 64, "bytes": 4, "description": "PIDs supported [$41 - $60]"},
    # {"command": b'0141\r\n', "dec": 65, "bytes": 4, "description": "Monitor status this drive cycle"},
    # {"command": b'0142\r\n', "dec": 66, "bytes": 2, "description": "Control module voltage"},
    # {"command": b'0143\r\n', "dec": 67, "bytes": 2, "description": "Absolute load value"},
    # {"command": b'0144\r\n', "dec": 68, "bytes": 2, "description": "Commanded Air-Fuel Equivalence Ratio (lambda)"},
    # {"command": b'0145\r\n', "dec": 69, "bytes": 1, "description": "Relative throttle position"},
    # {"command": b'0146\r\n', "dec": 70, "bytes": 1, "description": "Ambient air temperature"},
    # {"command": b'0147\r\n', "dec": 71, "bytes": 1, "description": "Absolute throttle position B"},
    # {"command": b'0148\r\n', "dec": 72, "bytes": 1, "description": "Absolute throttle position C"},
    # {"command": b'0149\r\n', "dec": 73, "bytes": 1, "description": "Accelerator pedal position D"},
    # {"command": b'014A\r\n', "dec": 74, "bytes": 1, "description": "Accelerator pedal position E"},
    # {"command": b'014B\r\n', "dec": 75, "bytes": 1, "description": "Accelerator pedal position F"},
    # {"command": b'014C\r\n', "dec": 76, "bytes": 1, "description": "Commanded throttle actuator"},
    # {"command": b'014D\r\n', "dec": 77, "bytes": 2, "description": "Time run with MIL on"},
    # {"command": b'014E\r\n', "dec": 78, "bytes": 2, "description": "Time since trouble codes cleared"},
    # {"command": b'014F\r\n', "dec": 79, "bytes": 4, "description": "Maximum value for Fuel–Air equivalence ratio, oxygen sensor voltage, oxygen sensor current, and intake manifold absolute pressure"},
    # {"command": b'0150\r\n', "dec": 80, "bytes": 4, "description": "Maximum value for air flow rate from mass air flow sensor"},
    # {"command": b'0151\r\n', "dec": 81, "bytes": 1, "description": "Fuel Type"},
    # {"command": b'0152\r\n', "dec": 82, "bytes": 1, "description": "Ethanol fuel %"},
    # {"command": b'0153\r\n', "dec": 83, "bytes": 2, "description": "Absolute Evap system Vapor Pressure"},
    # {"command": b'0154\r\n', "dec": 84, "bytes": 2, "description": "Evap system vapor pressure"},
    # {"command": b'0155\r\n', "dec": 85, "bytes": 2, "description": "Short term secondary oxygen sensor trim, A: bank 1, B: bank 3"},
    # {"command": b'0156\r\n', "dec": 86, "bytes": 2, "description": "Long term secondary oxygen sensor trim, A: bank 1, B: bank 3"},
    # {"command": b'0157\r\n', "dec": 87, "bytes": 2, "description": "Short term secondary oxygen sensor trim, A: bank 2, B: bank 4"},
    # {"command": b'0158\r\n', "dec": 88, "bytes": 2, "description": "Long term secondary oxygen sensor trim, A: bank 2, B: bank 4"},
    # {"command": b'0159\r\n', "dec": 89, "bytes": 2, "description": "Fuel rail absolute pressure"},
    # {"command": b'015A\r\n', "dec": 90, "bytes": 1, "description": "Relative accelerator pedal position"},
    # {"command": b'015B\r\n', "dec": 91, "bytes": 1, "description": "Hybrid battery pack remaining life"},
    # {"command": b'015C\r\n', "dec": 92, "bytes": 1, "description": "Engine oil temperature"},
    # {"command": b'015D\r\n', "dec": 93, "bytes": 2, "description": "Fuel injection timing"},
    # {"command": b'015E\r\n', "dec": 94, "bytes": 2, "description": "Engine fuel rate"},
    # {"command": b'015F\r\n', "dec": 95, "bytes": 1, "description": "Emission requirements to which vehicle is designed"},
    # {"command": b'0160\r\n', "dec": 96, "bytes": 4, "description": "PIDs supported [$61 - $80]"},
    # {"command": b'0161\r\n', "dec": 97, "bytes": 1, "description": "Driver's demand engine - percent torque"},
    # {"command": b'0162\r\n', "dec": 98, "bytes": 1, "description": "Actual engine - percent torque"},
    # {"command": b'0163\r\n', "dec": 99, "bytes": 2, "description": "Engine reference torque"},
    # {"command": b'0164\r\n', "dec": 100, "bytes": 5, "description": "Engine percent torque data"},
    # {"command": b'0165\r\n', "dec": 101, "bytes": 2, "description": "Auxiliary input / output supported"},
    # {"command": b'0166\r\n', "dec": 102, "bytes": 5, "description": "Mass air flow sensor"},
    # {"command": b'0167\r\n', "dec": 103, "bytes": 3, "description": "Engine coolant temperature"},
    # {"command": b'0168\r\n', "dec": 104, "bytes": 3, "description": "Intake air temperature sensor"},
    # {"command": b'0169\r\n', "dec": 105, "bytes": 7, "description": "Actual EGR, Commanded EGR, and EGR Error"},
    # {"command": b'016A\r\n', "dec": 106, "bytes": 5, "description": "Commanded Diesel intake air flow control and relative intake air flow position"},
    # {"command": b'016B\r\n', "dec": 107, "bytes": 5, "description": "Exhaust gas recirculation temperature"},
    # {"command": b'016C\r\n', "dec": 108, "bytes": 5, "description": "Commanded throttle actuator control and relative throttle position"},
    # {"command": b'016D\r\n', "dec": 109, "bytes": 11, "description": "Fuel pressure control system"},
    # {"command": b'016E\r\n', "dec": 110, "bytes": 9, "description": "Injection pressure control system"},
    # {"command": b'016F\r\n', "dec": 111, "bytes": 3, "description": "Turbocharger compressor inlet pressure"},
    # {"command": b'0170\r\n', "dec": 112, "bytes": 10, "description": "Boost pressure control"},
    # {"command": b'0171\r\n', "dec": 113, "bytes": 6, "description": "Variable Geometry turbo (VGT) control"},
    # {"command": b'0172\r\n', "dec": 114, "bytes": 5, "description": "Wastegate control"},
    # {"command": b'0173\r\n', "dec": 115, "bytes": 5, "description": "Exhaust pressure"},
    # {"command": b'0174\r\n', "dec": 116, "bytes": 5, "description": "Turbocharger RPM"},
    # {"command": b'0175\r\n', "dec": 117, "bytes": 7, "description": "Turbocharger temperature"},
    # {"command": b'0176\r\n', "dec": 118, "bytes": 7, "description": "Turbocharger temperature"},
    # {"command": b'0177\r\n', "dec": 119, "bytes": 5, "description": "Charge air cooler temperature (CACT)"},
    # {"command": b'0178\r\n', "dec": 120, "bytes": 9, "description": "Exhaust Gas temperature (EGT) Bank 1"},
    # {"command": b'0179\r\n', "dec": 121, "bytes": 9, "description": "Exhaust Gas temperature (EGT) Bank 2"},
    # {"command": b'017A\r\n', "dec": 122, "bytes": 7, "description": "Diesel particulate filter (DPF) differential pressure"},
    # {"command": b'017B\r\n', "dec": 123, "bytes": 7, "description": "Diesel particulate filter (DPF)"},
    # {"command": b'017C\r\n', "dec": 124, "bytes": 9, "description": "Diesel Particulate filter (DPF) temperature"},
    # {"command": b'017D\r\n', "dec": 125, "bytes": 1, "description": "NOx NTE (Not-To-Exceed) control area status"},
    # {"command": b'017E\r\n', "dec": 126, "bytes": 1, "description": "PM NTE (Not-To-Exceed) control area status"},
    # {"command": b'017F\r\n', "dec": 127, "bytes": 13, "description": "Engine run time [b]"},
    # {"command": b'0180\r\n', "dec": 128, "bytes": 4, "description": "PIDs supported [$81 - $A0]"},
    # {"command": b'0181\r\n', "dec": 129, "bytes": 41, "description": "Engine run time for Auxiliary Emissions Control Device(AECD)"},
    # {"command": b'0182\r\n', "dec": 130, "bytes": 41, "description": "Engine run time for Auxiliary Emissions Control Device(AECD)"},
    # {"command": b'0183\r\n', "dec": 131, "bytes": 9, "description": "NOx sensor"},
    # {"command": b'0184\r\n', "dec": 132, "bytes": 1, "description": "Manifold surface temperature"},
    # {"command": b'0185\r\n', "dec": 133, "bytes": 10, "description": "NOx reagent system"},
    # {"command": b'0186\r\n', "dec": 134, "bytes": 5, "description": "Particulate matter (PM) sensor"},
    # {"command": b'0187\r\n', "dec": 135, "bytes": 5, "description": "Intake manifold absolute pressure"},
    # {"command": b'0188\r\n', "dec": 136, "bytes": 13, "description": "SCR Induce System"},
    # {"command": b'0189\r\n', "dec": 137, "bytes": 41, "description": "Run Time for AECD #11-#15"},
    # {"command": b'018A\r\n', "dec": 138, "bytes": 41, "description": "Run Time for AECD #16-#20"},
    # {"command": b'018B\r\n', "dec": 139, "bytes": 7, "description": "Diesel Aftertreatment"},
    # {"command": b'018C\r\n', "dec": 140, "bytes": 17, "description": "O2 Sensor (Wide Range)"},
    # {"command": b'018D\r\n', "dec": 141, "bytes": 1, "description": "Throttle Position G"},
    # {"command": b'018E\r\n', "dec": 142, "bytes": 1, "description": "Engine Friction - Percent Torque"},
    # {"command": b'018F\r\n', "dec": 143, "bytes": 7, "description": "PM Sensor Bank 1 & 2"},
    # {"command": b'0190\r\n', "dec": 144, "bytes": 3, "description": "WWH-OBD Vehicle OBD System Information"},
    # {"command": b'0191\r\n', "dec": 145, "bytes": 5, "description": "WWH-OBD Vehicle OBD System Information"},
    # {"command": b'0192\r\n', "dec": 146, "bytes": 2, "description": "Fuel System Control"},
    # {"command": b'0193\r\n', "dec": 147, "bytes": 3, "description": "WWH-OBD Vehicle OBD Counters support"},
    # {"command": b'0194\r\n', "dec": 148, "bytes": 12, "description": "NOx Warning And Inducement System"},
    # {"command": b'0198\r\n', "dec": 152, "bytes": 9, "description": "Exhaust Gas Temperature Sensor"},
    # {"command": b'0199\r\n', "dec": 153, "bytes": 9, "description": "Exhaust Gas Temperature Sensor"},
    # {"command": b'019A\r\n', "dec": 154, "bytes": 6, "description": "Hybrid/EV Vehicle System Data, Battery, Voltage"},
    # {"command": b'019B\r\n', "dec": 155, "bytes": 4, "description": "Diesel Exhaust Fluid Sensor Data"},
    # {"command": b'019C\r\n', "dec": 156, "bytes": 17, "description": "O2 Sensor Data"},
    # {"command": b'019D\r\n', "dec": 157, "bytes": 4, "description": "Engine Fuel Rate"},
    # {"command": b'019E\r\n', "dec": 158, "bytes": 2, "description": "Engine Exhaust Flow Rate"},
    # {"command": b'019F\r\n', "dec": 159, "bytes": 9, "description": "Fuel System Percentage Use"},
    # {"command": b'01A0\r\n', "dec": 160, "bytes": 4, "description": "PIDs supported [$A1 - $C0]"},
    # {"command": b'01A1\r\n', "dec": 161, "bytes": 9, "description": "NOx Sensor Corrected Data"},
    # {"command": b'01A2\r\n', "dec": 162, "bytes": 2, "description": "Cylinder Fuel Rate"},
    # {"command": b'01A3\r\n', "dec": 163, "bytes": 9, "description": "Evap System Vapor Pressure"},
    # {"command": b'01A4\r\n', "dec": 164, "bytes": 4, "description": "Transmission Actual Gear"},
    # {"command": b'01A5\r\n', "dec": 165, "bytes": 4, "description": "Commanded Diesel Exhaust Fluid Dosing"},
    # {"command": b'01A6\r\n', "dec": 166, "bytes": 4, "description": "Odometer [c]"},
    # {"command": b'01A7\r\n', "dec": 167, "bytes": 4, "description": "NOx Sensor Concentration Sensors 3 and 4"},
    # {"command": b'01A8\r\n', "dec": 168, "bytes": 4, "description": "NOx Sensor Corrected Concentration Sensors 3 and 4"},
    # {"command": b'01A9\r\n', "dec": 169, "bytes": 4, "description": "ABS Disable Switch State"},
    # {"command": b'01C0\r\n', "dec": 192, "bytes": 4, "description": "PIDs supported [$C1 - $E0]"},
    # {"command": b'01C3\r\n', "dec": 195, "bytes": 2, "description": "Fuel Level Input A/B"},
    # {"command": b'01C4\r\n', "dec": 196, "bytes": 8, "description": "Exhaust Particulate Control System Diagnostic Time/Count"},
    # {"command": b'01C5\r\n', "dec": 197, "bytes": 4, "description": "Fuel Pressure A and B"},
    # {"command": b'01C6\r\n', "dec": 198, "bytes": 7, "description": "Particulate control - driver inducement system status"},
    # {"command": b'01C7\r\n', "dec": 199, "bytes": 2, "description": "Distance Since Reflash or Module Replacement"},
    # {"command": b'01C8\r\n', "dec": 200, "bytes": 1, "description": "NOx Control Diagnostic (NCD) and Particulate Control Diagnostic (PCD) Warning Lamp status"},
]

# Define ELM327 initialization commands with structured format
elm_commands = [
    {"command": b'ATZ\r\n', "description": "Reset"},
    {"command": b'ATE0\r\n', "description": "Turn echo off"},
    {"command": b'ATL0\r\n', "description": "Line feed off"},
    {"command": b'ATH1\r\n', "description": "Headers on"},
    {"command": b'ATST\r\n', "description": "Set timeout to 0 ms"},
    {"command": b'ATSP3\r\n', "description": "Set protocol to ISO 9141-2"},
    {"command": b'ATAL\r\n', "description": "Allow long messages"}
]


def decode_obd_rpm(command_string):
    if len(command_string) < 4:
        return "Invalid input"
    first_byte, second_byte = command_string[:2], command_string[2:4]
    try:
        rpm = (int(first_byte, 16) * 256 + int(second_byte, 16)) // 4
        print("Decoded RPM: {}".format(rpm))
        return rpm
    except ValueError:
        return "Invalid command string"

def read_response(serial_port):
    response = b''
    start_time = time.time()
    while time.time() - start_time < serial_port.timeout:
        buffer = serial_port.readline()
        if buffer:
            print("Received buffer: {}".format(buffer))
            response += buffer
    if response:
        print("Complete response received: {}".format(response))
    return response.strip()

def execute_command(serial_port, command):
    try:
        full_command = command['command'].encode('utf-8')
        print("Sending command: {}".format(full_command))
        serial_port.write(full_command)
        time.sleep(0.5)
        response = read_response(serial_port)
        decoded_response = response.decode('utf-8')
        print("Decoded response: {}".format(decoded_response))
        return decoded_response
    except serial.SerialException as e:
        error_message = "Serial exception: {}".format(str(e))
        print(error_message)
        return error_message

def execute_commands(serial_port, commands):
    results = []
    for cmd in commands:
        print("\nExecuting command for: {}".format(cmd['description']))
        response = execute_command(serial_port, cmd)
        results.append((cmd['description'], response))
    return results

def print_table(results):
    max_len = max(len(desc) for desc, resp in results)
    print("-" * (max_len + 32))
    print("| {:^{}} | Response".format("Command Description", max_len))
    print("-" * (max_len + 32))
    for desc, resp in results:
        print("| {:<{}} | {}".format(desc, max_len, resp))
    print("-" * (max_len + 32))

# Setup the serial connection
print("Initializing serial connection...")
serial_port = serial.Serial('/dev/ttyACM0', 38400, timeout=3)

# Execute ELM and ECU commands
elm_results = execute_commands(serial_port, elm_commands)
ecu_results = execute_commands(serial_port, pids)

# Display results in tables
print("\nELM327 Responses:")
print_table(elm_results)
print("\nECU Responses:")
print_table(ecu_results)

# Close the serial connection
print("Closing serial connection...")
serial_port.close()
