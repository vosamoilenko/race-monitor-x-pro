# -*- coding: utf-8 -*-

import time

from constants import ECU_COMMANDS, ELM_COMMANDS, PIDCommand
from pid_mapper import PIDMapper

import csv

def read_csv_last_column(filename):
    data = []

    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        current_array = []
        for i, row in enumerate(reader, 1):
            current_array.append([row[0], row[-1]])  # Append only the last column
            if i % 11 == 0:
                data.append(current_array)
                current_array = []

        if current_array:  # In case the number of rows is not a multiple of 11
            data.append(current_array)

    return data

filename = "/Users/vo1/Developer/github.com/vosamoilenko/race-monitor-x-pro/obd-rally-golf/logs-gran.csv"
result = read_csv_last_column(filename)
for arr in result:
    # print(arr)

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

    obj = {}
    for item in arr:
        obj[item[0]] = PIDMapper.mapHex(item[1])

    print(obj)


