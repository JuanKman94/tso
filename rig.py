#!/usr/bin/env python3

import sys
import random
import math

HELP = '''Random Instance Generator

Usage: {0} <n> <m> <capacity> <cost>-<range> [<K>]

Where:
    * <n> number of clients.
    * <m> number of facilities.
    * <capacity> fixed for each facility.
    * <cost> for transportation from facility to client; random number
      between <cost> and <range>.
    * <K> optional number instances to be generated, default 1.

Instances are written to file cflp_<n>_<m>_<capacity>_<cost>-<k>.dat,
where k is the instance number; the contents of such file is:

    <n> <m> <capacity>
    <clients demands>
    <facility-client costs matrix [n x m]>

Where <client capacity> is the random-generated capacity for client <i>,
for <i> from 1 through <n>. Each line is a client's capacity, thus the
instance file has a total of <n> + 1 lines.

Example: {0} 50 16 5000 75-100'''

def randint_list(n, _min, _max):
    l = list()

    for i in range(n):
        l.append( random.randint( _min, _max) )

    return l

def gen_clients_demands(n, m, m_cap):
    clients_demands = list()
    total_cap = m * m_cap
    top = int( total_cap / n )

    clients_demand = randint_list(n-1, math.floor(0.9 * top), math.ceil( 1.1 * top))

    # For the last client we substract the sum of all previous clients demands
    # from the total capacity
    x = - total_cap + sum( clients_demand )
    x = math.fabs( x )
    clients_demand.append( int( x ) )

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

n = math.floor( float(sys.argv[1]) )
m = math.floor( float(sys.argv[2]) )

cap = math.floor( float(sys.argv[3]) )

# Parse the cost of transportations
ran = sys.argv[4]
if ran.count('-') != 1:
    raise ValueError('Error parsing cost range.')
cost_min, cost_max = int(ran.split('-')[0]), int(ran.split('-')[1])

K = 1
if len( sys.argv) > 5: K = math.floor( float(sys.argv[5]) )

try:
    for k in range(K):
        fname = "cflp_{0}_{1}_{2}-{3}.dat".format(
                    n, m, cap, k+1
                )
        fhandle = open(fname, 'w')
        print('Generating instance {0}... '.format(fname), end='')

        inst = gen_clients_demands(n, m, cap)

        desc = '''{n} {m} {capacity}\n'''.format(
            n = n,
            m = m,
            capacity = cap
        )
        fhandle.write(desc)

        for i in range( len(inst) ):
            fhandle.write( "{0}\n".format(inst[i]) )

        costs_matrix = gen_instance_costs(n, m, cost_min, cost_max)

        # print the costs matrix to file
        for y in range( len(costs_matrix) ):
            line = ""
            l = costs_matrix[y]
            for x in range( len(l) ):
                line += str( l[x] ) + " "
            line = line.rstrip()

            fhandle.write("{line}\n".format(line = line))

        print('Done!')
        fhandle.close()
except IOError as ex:
    print('Error while trying to write file')
    print(ex)
#except Exception as ex:
#    print('Error while generating instances')
#    print(ex)
