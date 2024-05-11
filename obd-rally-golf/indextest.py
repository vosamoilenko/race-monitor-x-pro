# # -*- coding: utf-8 -*-

import csv
import json
from pid_mapper import PIDMapper
import datetime

def read_csv_last_column(filename):
    data = []

    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        current_array = []
        for i, row in enumerate(reader, 1):
            raw_date = row[1]
            dt = datetime.datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S")
            iso_format = dt.isoformat()

            current_array.append([row[0], row[-1], iso_format])  # Append first and last column

            if i % 11 == 0:
                data.append(current_array)
                current_array = []
        if current_array:  # In case the number of rows is not a multiple of 11
            data.append(current_array)

    # print(data)

    return data

filename = "/Users/vo1/Developer/github.com/vosamoilenko/race-monitor-x-pro/obd-rally-golf/logs-gran.csv"
result = read_csv_last_column(filename)
all_data = []

for arr in result:
    # Initialize an empty dictionary
    obj = {}
    # Assign values to the dictionary, checking if each element exists
    obj['monitorStatus'] = {
        'value': PIDMapper.mapHex(arr[0][1]) if len(arr) > 0 else None,
        'timestamp': arr[0][2] if len(arr) > 0 else None
    }
    obj['fuelSystemStatus'] = {
        'value': PIDMapper.mapHex(arr[1][1]) if len(arr) > 1 else None,
        'timestamp': arr[1][2] if len(arr) > 1 else None
    }
    obj['engineLoad'] = {
        'value': PIDMapper.mapHex(arr[2][1]) if len(arr) > 2 else None,
        'timestamp': arr[2][2] if len(arr) > 2 else None
    }
    obj['coolantTemperature'] = {
        'value': PIDMapper.mapHex(arr[3][1]) if len(arr) > 3 else None,
        'timestamp': arr[3][2] if len(arr) > 3 else None
    }
    obj['intakeManifoldPressure'] = {
        'value': PIDMapper.mapHex(arr[4][1]) if len(arr) > 4 else None,
        'timestamp': arr[4][2] if len(arr) > 4 else None
    }
    obj['engineSpeed'] = {
        'value': PIDMapper.mapHex(arr[5][1]) if len(arr) > 5 else None,
        'timestamp': arr[5][2] if len(arr) > 5 else None
    }
    obj['vehicleSpeed'] = {
        'value': PIDMapper.mapHex(arr[6][1]) if len(arr) > 6 else None,
        'timestamp': arr[6][2] if len(arr) > 6 else None
    }
    obj['timingAdvance'] = {
        'value': PIDMapper.mapHex(arr[7][1]) if len(arr) > 7 else None,
        'timestamp': arr[7][2] if len(arr) > 7 else None
    }
    obj['intakeAirTemperature'] = {
        'value': PIDMapper.mapHex(arr[8][1]) if len(arr) > 8 else None,
        'timestamp': arr[8][2] if len(arr) > 8 else None
    }
    obj['mafSensorAirFlowRate'] = {
        'value': PIDMapper.mapHex(arr[9][1]) if len(arr) > 9 else None,
        'timestamp': arr[9][2] if len(arr) > 9 else None
    }
    obj['throttlePosition'] = {
        'value': PIDMapper.mapHex(arr[10][1]) if len(arr) > 10 else None,
        'timestamp': arr[10][2] if len(arr) > 10 else None
    }
    
    # Append the dictionary to the list of all data
    # print(obj)
    all_data.append(obj)

# Write the collected data to a JSON file
json_filename = "./output.json"
with open(json_filename, 'w') as jsonfile:
    json.dump(all_data, jsonfile, indent=4)

print(f"Data successfully written to {json_filename}.")
