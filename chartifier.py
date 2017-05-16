#!/usr/bin/env python3

'''Read heur.py CSV results from STDIN, parse them and write them to a
ChartJS-compatible JSON file for visualization.
Default chartjs structure in `chart-template.json` and writeen to chartjs.json
'''

import sys
import json

HEUR = 1
KEY = 'default'

if len(sys.argv) > 1:
    HEUR = int( sys.argv[1] )

# key for output JSON
if len(sys.argv) > 2:
    KEY = str( sys.argv[2] )

arr = list()
x = 1

while True:
    try:
        line = input()
        values = line.split(',')
        total_cost = int( values[4].replace('"', '') )

        arr.append( { 'x': x, 'y': total_cost })
        x += 1
    except EOFError as ex:
        break

existing = 'chartjs.json'
template = 'chart-template.json'

try:
    existing_chart = open(existing, 'r')
    chartjs = json.load(existing_chart)
    existing_chart.close()
except IOError:
    chartjs = {}

try:
    chart_template = open(template, 'r')
    template = json.load(chart_template)
    chart_template.close()
except IOError:
    print('Error parsing json template')
    sys.exit(1)

try:
    chart = chartjs[KEY]
except KeyError:
    chartjs[KEY] = template
    chart = chartjs[KEY]

try:
    dataset = chart['data']['datasets'][HEUR-1]
except IndexError:
    dataset = { 'label': 'Heurística ' + str(HEUR), 'fill': False }
    chart['data']['datasets'].append( dataset )

dataset['data'] = arr

# update json file with new data
try:
    json_file = open('chartjs.json', 'w')
except IOError:
    json_file = None
    print('Error opening json for writing, printing to STDOUT')

json_str = json.dumps(chartjs, indent = 4, sort_keys = True)

if json_file:
    json_file.write(json_str)
else:
    print(json_str)


sys.exit(0)
