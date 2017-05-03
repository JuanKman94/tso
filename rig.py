#!/usr/bin/env python3

import sys
import random
import math

HELP = '''Random Instance Generator

Usage: {0} <n> <m> <capacity> <cost> [<K>]

Where:
    * <n> number of clients.
    * <m> number of facilities.
    * <capacity> for each facility.
    * <cost> fixed for each facility.
    * <K> optional number instances to be generated, default 1.

Instances are written to file cflp_<n>_<m>_<capacity>_<cost>-<k>.dat,
where k is the instance number; the contents of such file is:

    <n> <m> <capacity> <cost>
    <client capacity>

Where <client capacity> is the random-generated capacity for client <i>,
for <i> from 1 through <n>. Each line is a client's capacity, thus the
instance file has a total of <n> + 1 lines.

Example: {0} 50 16 5000 7500'''

def gen_instance(n, m, m_cap):
    clients_demand = list()
    total_cap = m * m_cap
    top = int( total_cap / n )

    for i in range(n - 1):
        x = random.randint( math.floor(0.9 * top), math.ceil( 1.1 * top) )
        clients_demand.append( x )

    # For the last client we substract the sum of all previous clients demands
    # from the total capacity
    x = - total_cap + sum( clients_demand )
    x = math.fabs( x )
    clients_demand.append( int( x ) )

    return clients_demand

if len( sys.argv ) < 5:
    print(HELP.format( sys.argv[0] ))
    sys.exit(1)

n = math.floor( float(sys.argv[1]) )
m = math.floor( float(sys.argv[2]) )

cap = math.floor( float(sys.argv[3]) )
cost = math.floor( float(sys.argv[4]) )

K = 1
if len( sys.argv) > 5: K = math.floor( float(sys.argv[5]) )

try:
    for k in range(K):
        fname = "cflp_{0}_{1}_{2}_{3}-{4}.dat".format(
                    n, m, cap, cost, k+1
                )
        fhandle = open(fname, 'w')
        print('Generating instance {0}... '.format(fname), end='')

        inst = gen_instance(n, m, cap)

        desc = '''{n} {m} {capacity} {cost}\n'''.format(
            n = n,
            m = m,
            capacity = cap,
            cost = cost
        )
        fhandle.write(desc)

        for i in range( len(inst) ):
            fhandle.write( "{0}\n".format(inst[i]) )

        print('Done!')
        fhandle.close()
except IOError as ex:
    print('Error while trying to write file')
    print(ex)
except Exception as ex:
    print('Error while generating instances')
    print(ex)
