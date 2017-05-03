#!/usr/bin/env python
# python 3

import sys
import random
import math

AYUDA = '''Generador de instancias aleatorias

Uso: {0} <n> <m> <capacidad> <costo>

Donde:
    * <n> es la cantidad de clientes.
    * <m> es la cantidad de plantas.
    * <capacidad> es la capacidad de cada planta.
    * <costo> es el costo fijo de cada planta.

Ejemplo: {0} 50 16 5000 7500'''

if len( sys.argv ) < 5:
    print(AYUDA.format( sys.argv[0] ))
    sys.exit(1)

# Cantidad de clientes
n = math.floor( float(sys.argv[1]) )
# Cantidad de proveedores/plantas
m = math.floor( float(sys.argv[2]) )

# Capacidad de planta
cap = math.floor( float(sys.argv[3]) )
CAP_TOTAL = m * cap
# Costo fijo de planta
costo = math.floor( float(sys.argv[4]) )

demandas = list()
top = int( CAP_TOTAL / n )

for i in range(n - 1):
    x = random.randint( math.floor(0.9 * top), math.ceil( 1.1 * top) )
    demandas.append( x )

# Para el ultimo numero restamos la suma de todas las demandas anteriores
# a la capacidad total
x = - CAP_TOTAL + sum( demandas )
x = math.fabs( x )
demandas.append( int( x ) )

status = '''Clientes: {cli}
Plantas: {pla}
Capacidad total: {tot}
Suma demandas: {dem}
Demandas: {lis}'''.format(
    cli = n,
    pla = m,
    tot = CAP_TOTAL,
    dem = sum(demandas),
    lis = demandas
)

print(status)
