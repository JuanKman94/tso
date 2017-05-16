#!/usr/bin/env python3

import sys
import random
import math

HELP = '''Random Instance Generator

Usage: {0} <m> <n> <plant-cost>-<range> <capacity> <demand>-<range> [<K>] [<dir>]

Where:
    * <m> number of facilities.
    * <n> number of clients.
    * <plant-cost> for keeping the plant open; random number
      between <cost> and <range>.
    * <capacity> fixed for each facility.
    * <cost> for transportation from facility to client; random number
      between <cost> and <range>.
    * <K> optional number instances to be generated, default 1.
    * <dir> optional directory to which write files, default CWD.

Instances are written to file cflp_<n>_<m>_<capacity>_<cost>-<k>.dat,
k is the instance number; the contents of such file is:

    <m> <n> <capacity>
    <plants costs>
    <facility-client costs matrix [n x m]>
    <clients demands>

<client demands> is the random-generated capacity for client <i>,
for <i> from 1 through <n>. Each line is a client's capacity.

Example: {0} 10 20 1500-2000 5000 75-100'''

def randint_list(n, _min, _max):
    l = list()

    for i in range(n):
        l.append( random.randint( _min, _max) )

    return l

def gen_clients_demands(n, m, m_cap):
    total_cap = m * m_cap
    top = int( total_cap / n ) - int( m_cap * 0.1)

    clients_demand = randint_list(n, math.floor(0.5 * top), top)

    #clients_demand = randint_list(n-1, math.floor(0.7 * top), top)
    # For the last client we substract the sum of all previous clients demands
    # from the total capacity
    #x = - total_cap + sum( clients_demand )
    #x = math.fabs( x )
    #clients_demand.append( int( x ) )

    return clients_demand

def gen_instance_costs(n_clients, n_facilities, _min, _max):
    l = list()

    for y in range(n_facilities):
        l.append( randint_list(n_clients, _min, _max) )

    return l


############### Main ###############

if len( sys.argv ) < 5:
    print(HELP.format( sys.argv[0] ))
    sys.exit(1)

m = math.floor( float(sys.argv[1]) )
n = math.floor( float(sys.argv[2]) )

# Parse the cost of transportations
ran = sys.argv[3]
if ran.count('-') != 1:
    raise ValueError('Error parsing cost range.')
plant_cost_min, plant_cost_max = int(ran.split('-')[0]), int(ran.split('-')[1])

cap = math.floor( float(sys.argv[4]) )

# Parse the cost of transportations
ran = sys.argv[5]
if ran.count('-') != 1:
    raise ValueError('Error parsing cost range.')
cost_min, cost_max = int(ran.split('-')[0]), int(ran.split('-')[1])

K = 1
if len( sys.argv) > 6: K = math.floor( float(sys.argv[6]) )

OUTPUT_DIR = '.'
if len( sys.argv) > 7: OUTPUT_DIR = str(sys.argv[7])

try:
    for k in range(K):
        fname = "{out_dir}/cflp_{0}_{1}_{2}-{3}.dat".format(
                    m, n, cap, k+1, out_dir = OUTPUT_DIR
                )
        fhandle = open(fname, 'w')
        print('Generating instance {0}... '.format(fname), end='')

        desc = '''{n} {m} {capacity}\n'''.format(
            n = n,
            m = m,
            capacity = cap
        )
        fhandle.write(desc)

        plants_costs = randint_list(m, plant_cost_min, plant_cost_max)
        for i in range( len(plants_costs) ):
            fhandle.write( "{0}\n".format(plants_costs[i]) )

        costs_matrix = gen_instance_costs(n, m, cost_min, cost_max)

        # print the costs matrix to file
        for y in range( len(costs_matrix) ):
            line = ""
            l = costs_matrix[y]
            for x in range( len(l) ):
                line += str( l[x] ) + " "
            line = line.rstrip()

            fhandle.write("{line}\n".format(line = line))

        inst = gen_clients_demands(n, m, cap)
        for i in range( len(inst) ):
            fhandle.write( "{0}\n".format(inst[i]) )

        print('Done!')
        fhandle.close()
except IOError as ex:
    print('Error while trying to write file')
    print(ex)
#except Exception as ex:
#    print('Error while generating instances')
#    print(ex)
