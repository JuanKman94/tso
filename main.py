#!/usr/bin/env python3
import cflp

if __name__ == '__main__':
    problem = bcflp.read_instance(sys.argv[1] or 'cflp_5_10_5000-1.dat')
    print(problem)
