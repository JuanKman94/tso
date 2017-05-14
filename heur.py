#!/usr/bin/env python3

import sys
import cflp

PRINT_HEADERS = False

if len( sys.argv ) < 2:
    print('Error: instance filename required')
    sys.exit(-1)

fname = sys.argv[1]
inst = cflp.CFLProblem.from_instance(fname)

try:
    if sys.argv.index('--headers'):
        PRINT_HEADERS = True
except ValueError:
    '--headers not in list' # null statement

def print_heur_stats(inst, X, Y, heur = None):
    s = ""

    # facilities operations costs
    C_f = cflp.total_facilities_cost(inst, Y)
    # transportation costs
    C_t = cflp.total_transportation_cost(inst, X)

    # count operating/open facilities
    operating = 0
    for i in range(len(Y)):
        if Y[i] == 1: operating += 1

    if heur: s = '"' + str(heur) + '", '
    s += '"{operating}","{operations}","{transportation}","{total}","{y}"'.format(
            operating = operating,
            operations = C_f,
            transportation = C_t,
            total = C_f + C_t,
            y = Y
            )

    print(s)

############### Main ###############

if PRINT_HEADERS:
    print('heuristic,facilities,operations,transportation,total,solution')

#### Heuristic 1 ####
h1_X = cflp.CFLProblem.attendance_matrix(inst.n, inst.m)
h1_Y = cflp.CFLProblem.operating_facilities_list(inst.m)

(inst, h1_X, h1_Y) = cflp.heur_sorted_facility_costs(inst, h1_X, h1_Y)

print_heur_stats(inst, h1_X, h1_Y, 1)

## End Heuristic 1 ##

#### Heuristic 2 ####
#h2_X = cflp.CFLProblem.attendance_matrix(inst.n, inst.m)
#h2_Y = cflp.CFLProblem.operating_facilities_list(inst.m)
#
#(inst, h2_X, h2_Y) = cflp.heur_sorted_transportation_costs(inst, h2_X, h2_Y)
#
#print_heur_stats(inst, h2_X, h2_Y, 2)

## End Heuristic 2 ##
