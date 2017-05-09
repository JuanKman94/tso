#!/usr/bin/env python3

import sys
import cflp

if len( sys.argv ) < 2:
    print('Error: instance filename required')
    sys.exit(-1)

fname = sys.argv[1]
inst = cflp.CFLProblem.from_instance(fname)
#print(inst)

############### Main ###############

#### Heuristic 1 ####
h1_X = cflp.CFLProblem.attendance_matrix(inst.n, inst.m)
h1_Y = cflp.CFLProblem.operating_facilities_list(inst.m)

(inst, h1_X, h1_Y) = cflp.heur_sorted_facility_costs(inst, h1_X, h1_Y)

h1_C_f = cflp.total_facilities_cost(inst, h1_Y)
h1_C_t = cflp.total_transportation_cost(inst, h1_X)

status = '''Facilities costs: $ {0}
Transportation costs: $ {1}
Total: $ {2}'''.format(
    h1_C_f,
    h1_C_t,
    h1_C_f + h1_C_t
)
print(status)
print(h1_Y)

## End Heuristic 1 ##
