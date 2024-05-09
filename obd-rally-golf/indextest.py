# # -*- coding: utf-8 -*-

import csv
import json
from pid_mapper import PIDMapper

def read_csv_last_column(filename):
    data = []

    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        current_array = []
        for i, row in enumerate(reader, 1):
            current_array.append([row[0], row[-1]])  # Append first and last column
            if i % 11 == 0:
                data.append(current_array)
                current_array = []

        if current_array:  # In case the number of rows is not a multiple of 11
            data.append(current_array)

    return data

filename = "/Users/vo1/Developer/github.com/vosamoilenko/race-monitor-x-pro/obd-rally-golf/logs-gran.csv"
result = read_csv_last_column(filename)
all_data = []

for arr in result:
    # Initialize an empty dictionary
    obj = {}
    # Assign values to the dictionary, checking if each element exists
    obj['monitorStatus'] = PIDMapper.mapHex(arr[0][1]) if len(arr) > 0 else None
    obj['fuelSystemStatus'] = PIDMapper.mapHex(arr[1][1]) if len(arr) > 1 else None
    obj['engineLoad'] = PIDMapper.mapHex(arr[2][1]) if len(arr) > 2 else None
    obj['coolantTemperature'] = PIDMapper.mapHex(arr[3][1]) if len(arr) > 3 else None
    obj['intakeManifoldPressure'] = PIDMapper.mapHex(arr[4][1]) if len(arr) > 4 else None
    obj['engineSpeed'] = PIDMapper.mapHex(arr[5][1]) if len(arr) > 5 else None
    obj['vehicleSpeed'] = PIDMapper.mapHex(arr[6][1]) if len(arr) > 6 else None
    obj['timingAdvance'] = PIDMapper.mapHex(arr[7][1]) if len(arr) > 7 else None
    obj['intakeAirTemperature'] = PIDMapper.mapHex(arr[8][1]) if len(arr) > 8 else None
    obj['mafSensorAirFlowRate'] = PIDMapper.mapHex(arr[9][1]) if len(arr) > 9 else None
    obj['throttlePosition'] = PIDMapper.mapHex(arr[10][1]) if len(arr) > 10 else None
    
    # Append the dictionary to the list of all data
    # print(obj)
    all_data.append(obj)

# Write the collected data to a JSON file
json_filename = "./output.json"
with open(json_filename, 'w') as jsonfile:
    json.dump(all_data, jsonfile, indent=4)

print(f"Data successfully written to {json_filename}.")
