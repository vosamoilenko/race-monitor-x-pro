# -*- coding: utf-8 -*-

import serial
import time

from constants import ECU_COMMANDS, ELM_COMMANDS, PIDCommand
from pid_mapper import PIDMapper

# PIDMapper.map(PIDCommand.MONITOR_STATUS, "410100000000F5")
# PIDMapper.map(PIDCommand.ENGINE_LOAD, "4104FFF7")
# PIDMapper.map(PIDCommand.COOLANT_TEMPERATURE, "41056D66")
# PIDMapper.map(PIDCommand.INTAKE_MANIFOLD_PRESSURE, "410B6463")
# PIDMapper.map(PIDCommand.ENGINE_SPEED, "410C247094")
# PIDMapper.map(PIDCommand.VEHICLE_SPEED, "410D0001")
# PIDMapper.map(PIDCommand.TIMING_ADVANCE, "410EFF01")
# PIDMapper.map(PIDCommand.INTAKE_AIR_TEMPERATURE, "410F5D60")
# PIDMapper.map(PIDCommand.MAF_SENSOR_AIR_FLOW_RATE, "4110000004")
# PIDMapper.map(PIDCommand.THROTTLE_POSITION, "41110005")

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
        full_command = command['command']
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

def execute_ecu_commands(serial_port, commands):
    try:
        with open("ecu_commands_output.txt", "a") as f:
            while True:
                for cmd in commands:
                    command_name = cmd['command']
                    print("\nExecuting command for: {}".format(command_name))
                    try:
                        timestamp = time.time()
                        response = execute_command(serial_port, cmd)
                        f.write("Timestamp: {}\n".format(timestamp))
                        f.write("Command: {}\n".format(command_name))
                        f.write("Response: {}\n".format(response))
                    except Exception as e:
                        print("An error occurred for command {}: {}".format(command_name, e))
                time.sleep(1)  # Execute the commands every second
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print("An error occurred: {}".format(e))

def execute_commands(serial_port, commands):
    results = []
    for cmd in commands:
        print("\nExecuting command for: {}".format(cmd['description']))
        response = execute_command(serial_port, cmd)
        results.append((cmd['description'], response))
    return results

# Setup the serial connection
print("Initializing serial connection...")
serial_port = serial.Serial('/dev/ttyACM0', 38400, timeout=7)

# Execute ELM and ECU commands
elm_results = execute_commands(serial_port, ELM_COMMANDS)
serial_port.timeout = 3

# ecu_results = execute_commands(serial_port, ECU_COMMANDS)
with open("logs.txt", "w") as file:
    # Write data to the file
    while True:
        for cmd in ECU_COMMANDS:
            print("\nExecuting command for: {}".format(cmd['description']))
            response = execute_command(serial_port, cmd)
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            file.write("{}, {}, {}\n".format(cmd['command'], current_time, response))



Display results in tables
print("\nELM327 Responses:")
print_table(elm_results)
print("\nECU Responses:")
print_table(ecu_results)

Close the serial connection
print("Closing serial connection...")
serial_port.close()
