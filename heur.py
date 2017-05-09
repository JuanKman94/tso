#!/usr/bin/env python3

import sys
import cflp

if len( sys.argv ) < 2:
    print('Error: instance filename required')
    sys.exit(-1)

fname = sys.argv[1]
inst = cflp.CFLProblem.from_instance(fname)
#print(inst)

def print_heur_stats(inst, X, Y):
    # facilities operations costs
    C_f = cflp.total_facilities_cost(inst, Y)
    # transportation costs
    C_t = cflp.total_transportation_cost(inst, X)

    s = 'Costs: Facilities/Transportation (Total)' \
        ' | ${0} / ${1} (${2})' \
        ' | {3}'

    print(s.format(C_f, C_t, C_f + C_t, Y))

############### Main ###############

#### Heuristic 1 ####
h1_X = cflp.CFLProblem.attendance_matrix(inst.n, inst.m)
h1_Y = cflp.CFLProblem.operating_facilities_list(inst.m)

(inst, h1_X, h1_Y) = cflp.heur_sorted_facility_costs(inst, h1_X, h1_Y)

print('Heur 1  |  ', end='')
print_heur_stats(inst, h1_X, h1_Y)

## End Heuristic 1 ##

#### Heuristic 2 ####
h2_X = cflp.CFLProblem.attendance_matrix(inst.n, inst.m)
h2_Y = cflp.CFLProblem.operating_facilities_list(inst.m)

(inst, h2_X, h2_Y) = cflp.heur_sorted_transportation_costs(inst, h2_X, h2_Y)

print('Heur 2  |  ', end='')
print_heur_stats(inst, h2_X, h2_Y)

## End Heuristic 2 ##
