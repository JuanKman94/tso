import sys
import numpy

class CFLProblem():
    def __init__(self, n, m, facilities_costs, m_cap, clients, transportation_costs):
        self.n = n
        self.m = m
        self.facilities_costs = facilities_costs
        self.m_cap = m_cap
        self.clients = clients
        self.transportation_costs = transportation_costs

    def __str__(self):
        s = "Clients: {0}\n".format(self.n)
        s += "Facilities: {0}\n".format(self.m)
        s += "Facilities costs: ({0}) {1}\n".format(sum(self.facilities_costs), self.facilities_costs)
        s += "Fixed facility capacity: {0} ({1})\n".format(self.m_cap, self.m * self.m_cap)
        s += "Transportation costs: {0}\n".format(self.transportation_costs)
        s += "Clients: ({0}) {1}".format(sum(self.clients), self.clients)

        return s

    def asc_sorted_costs(self):
        '''Return ascending sorted indexes of facilities costs'''
        f_costs = list()
        sorted_costs = list()

        for i in range( len(self.facilities_costs) ):
            f_costs.append( self.facilities_costs[i] )
        f_costs.sort()

        for i in range( len(f_costs) ):
            sorted_costs.append(
                self.facilities_costs.index(f_costs[i])
            )

        return sorted_costs

    @classmethod
    def attendance_matrix(cls, n, m):
        '''Return an [m x n] attendance matrix.
            m[j][i] = 1 if plant j attends client i,
            m[j][i] = 0 otherwise'''
        return numpy.zeros( (m, n), dtype=numpy.int)

    @classmethod
    def operating_facilities_list(cls, m):
        '''Return a list with m integers with value 0'''
        return numpy.zeros( m, dtype=numpy.int)

    @classmethod
    def from_instance(cls, fname):
        '''Return object with data loaded from instance file'''
        clients = list()
        n, m, m_cap = 1, 1, 1
        facilities_costs, costs_matrix = list([ list() ]), list([ list() ])

        try:
            fhandle = open(fname, 'r')

            # read the instance meta data
            line = fhandle.readline()
            values = line.strip().split()

            n, m, = int(values[0]), int(values[1])
            m_cap = int(values[2])

            facilities_costs = list()
            costs_matrix = list()

            # read the facilities costs
            for y in range(m):
                line = fhandle.readline()
                facilities_costs.append( int(line) )

            # read the transportation costs
            for y in range(m):
                fac_costs = list()
                line = fhandle.readline()
                _costs = line.rstrip().split()
                for x in range( len(_costs) ):
                    fac_costs.append( int(_costs[x]) )

                costs_matrix.append( fac_costs )

            # read the clients demands
            for i in range(n):
                line = fhandle.readline()
                clients.append( int(line) )

            fhandle.close()
        except IOError as ex:
            print('There was an error reading the instance')
            raise Exception
            sys.exit(1)

        return cls(n, m, facilities_costs, m_cap, clients, costs_matrix)

def capacity_spent(inst, X, j):
    '''Total capacity spent for facility j

    @param  inst CFLProblem
    @param  X CFLProblem.attendance_matrix
    @param  j facility index
    @return int
    '''
    spent = 0

    for i in range( len(inst.clients) ):
        if X[j][i] == 1:
            spent += inst.clients[i]

    return spent

def client_attended(X, i):
    '''Return whether or not client i is attended

    @param  X CFLProblem.attendance_matrix
    @param  i client index
    @return bool
    '''
    for j in range( len(X) ):
        if X[j][i] == 1:
            return True

    return False

def total_facilities_cost(cflproblem, Y):
    cost = 0
    try:
        for j in range( len(Y) ):
            if Y[j] == 1:
                cost += cflproblem.facilities_costs[j]
    except IndexError as ex:
        print("Error calculating facilities costs. Incomplete calculation")

    return cost

def total_transportation_cost(cflproblem, X):
    cost = 0

    try:
        for x in range( len(X) ):
            row = X[x]
            for y in range( len(row) ):
                if X[x][y] == 1:
                    cost += cflproblem.transportation_costs[x][y]
    except IndexError as ex:
        print("Error calculating transportation costs. Incomplete calculation")

    return cost

def heur_sorted_facility_costs(inst, X, Y):
    '''Heuristic to solve CFLP by sorting facilities by their operating cost
    in ascending order, and then picking their clients as they can.

    @param  inst CFLProblem
    @param  X CFLProblem.attendance_matrix
    @param  Y CFLProblem.operating_facilities_list
    @return tuple (inst, X, Y)
    '''
    f_costs = inst.asc_sorted_costs()

    for y in range( inst.m ):
        j = f_costs[y]
        #print('Filling facility {0}'.format(j))

        for x in range( inst.n ):

            if client_attended(X, x) == True: continue

            spent = capacity_spent(inst, X, j)
            demand = inst.clients[x]
            attendable = (spent + demand <= inst.m_cap)

            #print('j = {j}; i = {i}; demand = {d}; occupied = {o}; total = {t}'.format(
            #    i = x,
            #    j = j,
            #    d = demand,
            #    o = spent,
            #    t = demand + spent
            #))

            if attendable == True:
                X[j][x] = 1
                Y[j] = 1

    return (inst, X, Y)