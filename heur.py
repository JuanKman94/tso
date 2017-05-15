#!/usr/bin/env python3

import sys
import cflp

PRINT_HEADERS = False
HEUR = 1

if len( sys.argv ) < 2:
    print('Error: instance filename required')
    sys.exit(-1)
elif len( sys.argv ) > 2:
    try:
        heur_number = int(sys.argv[2])
    except ValueError:
        'Error parsing heurisitic ID (number) to run' # null statement
        heur_number = 1
    finally:
        HEUR = heur_number

fname = sys.argv[1]
(inst, Y, X) = cflp.CFLProblem.from_instance(fname)

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

def write_heur_solution(inst, Y, X):
    fname = 'cflp_{0}_{1}_{2}-solution.dat'.format(
                inst.n, inst.m, inst.m_cap
            )
    try:
        fhandle = open(fname, 'w')


        desc = '{n} {m} {cap}'.format(
                    n = inst.n, m = inst.m, cap = inst.m_cap
                )
        fhandle.write("{0}\n".format(desc))

        for i in range( len(inst.facilities_costs) ):
            fhandle.write("{0}\n".format(inst.facilities_costs[i]))

        # print the costs matrix
        for j in range( len(inst.transportation_costs) ):
            line = ""
            # list for cost for each client
            l = inst.transportation_costs[j]
            for i in range( len(l) ):
                line += str( l[i] ) + " "

            line = line.rstrip()
            fhandle.write("{0}\n".format(line))

        # print clients' demands
        for i in range( len(inst.clients) ):
            fhandle.write("{0}\n".format(inst.clients[i]))

        # print open facilities matrix
        _y = ""
        for j in range( len(Y) ):
            _y += str( Y[j] ) + " "
        _y = _y.rstrip()
        fhandle.write("{0}\n".format(_y))

        # print distribution matrix `X`
        for j in range( len(X) ):
            line = ""
            # list for cost for each client
            l = X[j]
            for i in range( len(l) ):
                line += str( l[i] ) + " "

            line = line.rstrip()
            fhandle.write("{0}\n".format(line))

        fhandle.close()
    except IOError:
        print('Error while writing solution file')
        sys.exit(-1)

    return 0

############### Main ###############

if PRINT_HEADERS:
    print('heuristic,facilities,operations,transportation,total,solution')


result_X = cflp.CFLProblem.attendance_matrix(inst.n, inst.m)
result_Y = cflp.CFLProblem.operating_facilities_list(inst.m)

if HEUR == 1:
    #### Heuristic 1 ####
    (inst, result_X, result_Y) = cflp.heur_sorted_facility_costs(inst, result_X, result_Y)

    if not inst.is_valid(result_X, result_Y):
        print('No feasible solution found')
        sys.exit(1)
    ## End Heuristic 1 ##
else:
    #### Heuristic 2 ####
    (inst, result_X, result_Y) = cflp.heur_sorted_transportation_costs(inst, result_X, result_Y)

    if not inst.is_valid(result_X, result_Y):
        print('No feasible solution found')
        sys.exit(1)
    ## End Heuristic 2 ##

print_heur_stats(inst, result_X, result_Y, HEUR)

try:
    pos = sys.argv.index('--write')
    write_heur_solution(inst, result_Y, result_X)
except ValueError:
    'No write parameter passed'
