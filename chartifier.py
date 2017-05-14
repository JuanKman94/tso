#!/usr/bin/env python3

'''Read heur.py CSV results from STDIN, parse them and write them to a
ChartJS-compatible JSON file for visualization.
Default chartjs structure in `chart-template.json` and writeen to chartjs.json
'''

import sys
import json

HEUR = 1

if len(sys.argv) > 1:
    HEUR = int( sys.argv[1] )

arr = list()
x = 1

while True:
    try:
        line = input()
        values = line.split(',')
        y = int( values[4].replace('"', '') )

        arr.append( { 'x': x, 'y': y })
        x += 1
    except EOFError as ex:
        break

try:
    chart_file = open('chart-template.json', 'r')
    chart = json.load(chart_file)
except Exception as ex:
    print('Error parsing chartjs json')
    sys.exit(1)

# close json file to write to it later
chart_file.close()

try:
    dataset = chart['data']['datasets'][HEUR-1]
except IndexError:
    dataset = { 'label': 'Heuristica ' + str(HEUR), 'fill': False }
    chart['data']['datasets'].append( dataset )

dataset['data'] = arr

# update json file with new data
try:
    json_file = open('chartjs.json', 'w')
except IOError:
    json_file = None
    print('Error opening json for writing, printing to STDOUT')

json_str = json.dumps(chart, indent = 4, sort_keys = True)

if json_file:
    json_file.write(json_str)
else:
    print(json_str)


sys.exit(0)
