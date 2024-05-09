import serial
import time


def decode_obd_rpm(hex_string):
    # Ensure the string is long enough
    if len(hex_string) < 4:
        return "Invalid input"
    
    # Extract the relevant bytes (two pairs)
    first_byte = hex_string[:2]
    second_byte = hex_string[2:4]
    
    try:
        # Convert hex to integers
        first_value = int(first_byte, 16)
        second_value = int(second_byte, 16)
        
        # Calculate RPM according to OBD-II protocol
        rpm_value = (first_value * 256 + second_value) // 4
        
        return rpm_value
    except ValueError:
        return "Invalid hex string"


# ELM327 Commands
elm_commands = [
    (b'ATZ\r\n', "Reset"),
    (b'ATE0\r\n', "Turn echo off"),
    (b'ATL0\r\n', "Line feed off"),
    (b'ATST00\r\n', "Set timeout to 0 ms"),
    (b'ATSP3\r\n', "Set protocol to ISO 9141-2"),
    (b'ATAL\r\n', "Allow long messages")
]

# ECU Commands
ecu_commands = [
    (b'0100\r\n', "Supported PIDs"),
    (b'0101\r\n', "MIL Status")
]

# Function to read the response from the serial port
def read_response(serial_port):
    response = b''
    start_time = time.time()
    while time.time() - start_time < serial_port.timeout:
        buffer = serial_port.readline()  # Read a line from the serial port
        if not buffer:
            continue  # If no data is read, continue polling until the timeout is reached
        response += buffer
    return response.strip()  # Remove leading/trailing whitespace

# Function to convert the RPM response into an integer value
def parse_rpm(response):
    try:
        # Locate '41 0C' in the response, ignoring other parts
        start_idx = response.find('41 0C')
        if start_idx != -1:
            data_str = response[start_idx + 5:].split()  # Offset to start after '41 0C'
            if len(data_str) >= 2:
                # Extract the two bytes and convert them to RPM
                byte1 = int(data_str[0], 16)
                byte2 = int(data_str[1], 16)
                rpm_value = (byte1 * 256 + byte2) // 4
                return rpm_value
    except (ValueError, IndexError):
        pass
    return "Invalid response"

def parse_rpm1(response):
    try:
        # Locate '41 0C' in the response, ignoring other parts
        print("!!! ({})".format(response))
        # start_idx = response.find('410C')
        value_to_parse = response.split('410C')[1]
        return decode_obd_rpm(value_to_parse)
        
        # if start_idx != -1:
        #     data_str = response[start_idx + 5:].split()  # Offset to start after '41 0C'
        #     if len(data_str) >= 2:
        #         # Extract the two bytes and convert them to RPM
        #         byte1 = int(data_str[0], 16)
        #         byte2 = int(data_str[1], 16)
        #         rpm_value = (byte1 * 256 + byte2) // 4
        #         return rpm_value
    except (ValueError, IndexError):
        pass
    return "Invalid response"

# def executeCommand(command):
    

# Setup the serial connection
serial_port = serial.Serial('/dev/ttyACM0', 38400, timeout=10)  # Increased timeout for better response

# Execute each ELM command and print the response
print("Executing ELM327 Commands:")
for command, description in elm_commands:
    serial_port.write(command)
    time.sleep(0.5)  # Adding a slight delay for each command
    response = read_response(serial_port)
    print("({}) {}: {}".format(command.strip(), description, response))

# Execute each ECU command and print the response
serial_port.timeout = 2
print("\nExecuting ECU Commands:")
for command, description in ecu_commands:
    serial_port.write(command)
    time.sleep(0.5)  # Adding a slight delay between commands
    response = read_response(serial_port)
    print("({}) {}: {}".format(command.strip(), description, response))

# Start polling RPM every second with improved parsing
rpm_command = b'010C\r\n'
print("\nPolling RPM every second:")
try:
    while True:
        serial_port.write(rpm_command)
        time.sleep(0.5)  # Add delay to ensure data is returned before reading
        rpm_response = read_response(serial_port)
        print("(010C) Raw Response: {}".format(rpm_response))
        rpm_value1 = parse_rpm1(rpm_response)
        print("(010C) RPM1: {}".format(rpm_value1))
        time.sleep(1)


except KeyboardInterrupt:
    print("\nPolling stopped by user")

# Close the serial connection
serial_port.close()

