import sys
import numpy

class CFLProblem():
    def __init__(self, m, n, facilities_costs, m_cap, clients, transportation_costs):
        self.n = n # int
        self.m = m # int
        self.facilities_costs = facilities_costs # list(int)
        self.m_cap = m_cap # int
        self.clients = clients # list(int)
        self.transportation_costs = transportation_costs # list( list(int) )

    def __str__(self):
        s = "Facilities: {0}\n".format(self.m)
        s += "Clients: {0}\n".format(self.n)
        s += "Fixed facility capacity: {0} ({1})\n".format(self.m_cap, self.m * self.m_cap)
        s += "Facilities costs: ({0}) {1}\n".format(sum(self.facilities_costs), self.facilities_costs)
        s += "Clients: ({0}) {1}\n".format(sum(self.clients), self.clients)
        s += "Transportation costs: {0}".format(self.transportation_costs)

        return s

    def is_valid(self, X, Y):
        '''Return whether the given solution is valid according constraints
        facilities_can_supply and enough_capacity
        '''
        return self.facilities_can_supply(X) and self.enough_capacity(Y)

    # paper's model formula 3
    def facilities_can_supply(self, X):
        '''Validate each facility can supply their assigned clients'''
        for x in range( len(X) ):
            j = X[x]
            demand_j = 0 # demand for facility j
            for i in range( len(j) ):
                if j[i] == 1: # if facility j serves client i
                    demand_j += self.clients[i] # add client's demand

            # if facility's capacity can't cover the assigned demand
            if self.m_cap < demand_j:
                return False

        return True

    # paper's model formula 4
    def enough_capacity(self, Y):
        '''Validate every client has their demands fulfilled'''
        total_demand = sum(self.clients)
        opened_facilities = 0

        for y in range( len(Y) ):
            if Y[y] == 1: # if facility y is open
                opened_facilities += 1

        total_supply = opened_facilities * self.m_cap

        return total_supply >= total_demand

    def all_clients_served(self, X):
        clients = numpy.zeros(self.n, dtype=numpy.int)

        for i in range( len(X) ):
            for j in range( len(X[i]) ):
                if X[i][j] == 1:
                    clients[j] = 1

        for i in range( self.n ):
            if clients[i] == 0: return False
        return True

    def sorted_facilities(self, reverse = False):
        '''Return sorted indexes of facilities costs'''
        f_costs = list()
        _sorted = list()

        for i in range( len(self.facilities_costs) ):
            f_costs.append( self.facilities_costs[i] )
        f_costs.sort(reverse = reverse)

        for i in range( len(f_costs) ):
            _sorted.append(
                self.facilities_costs.index(f_costs[i])
            )

        return _sorted

    def sorted_transportation(self, reverse = False):
        '''Return sorted matrix [n x m] of transportations costs'''
        f_costs = list()
        _sorted = list()

        for i in range( len(self.transportation_costs) ):
            row = self.transportation_costs[i]
            f_costs.append( (sum(row), row) )
        f_costs.sort(reverse = reverse)

        for i in range( len(f_costs) ):
            _sorted.append(
                self.transportation_costs.index(f_costs[i][1])
            )

        return _sorted

    @classmethod
    def attendance_matrix(cls, m, n):
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
        '''Return tubple with CFLProblem instance from file plus
        Y and X solutions matrix, filled when available'''
        clients = list()
        n, m, m_cap = 1, 1, 1
        facilities_costs, costs_matrix = list([ list() ]), list([ list() ])
        Y = None
        X = None

        try:
            fhandle = open(fname, 'r')

            # read the instance meta data
            line = fhandle.readline()
            values = line.strip().split()

            m, n = int(values[0]), int(values[1])
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

            # attempt to read solution matrix
            _Y = fhandle.readline()

            if _Y != '':
                # recreate them with appropiate length
                Y = numpy.zeros(m, dtype=numpy.int)
                X = numpy.zeros((m, n), dtype=numpy.int)

                _Y = _Y.split()
                for j in range(len(_Y)):
                    Y[j] = int(_Y[j])

                # read distributions matrix
                for j in range(m):
                    _x = fhandle.readline()
                    _x = _x.split()
                    for i in range( len(_x) ):
                        X[j][i] = _x[i]

            fhandle.close()
        except IOError as ex:
            print('There was an error reading the instance')
            raise Exception
            sys.exit(1)

        instance = cls(m, n, facilities_costs, m_cap, clients, costs_matrix)
        return (instance, Y, X)





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

def facilities_cost(cflproblem, Y):
    cost = 0
    try:
        for j in range( len(Y) ):
            if Y[j] == 1:
                cost += cflproblem.facilities_costs[j]
    except IndexError as ex:
        print("Error calculating facilities costs. Incomplete calculation")

    return cost

def facility_transportation_cost(cflproblem, X, j):
    '''Calculate transportation costs for facility j given transportation matrix X'''
    cost = 0

    for y in range( len(X[j]) ):
        if X[j][y] == 1:
            cost += cflproblem.transportation_costs[j][y]

    return cost


def transportation_cost(cflproblem, X):
    cost = 0

    try:
        for x in range( len(X) ):
            for y in range( len(X[x]) ):
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
    f_costs = inst.sorted_facilities()

    for y in range( inst.m ):
        j = f_costs[y]

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

def heur_sorted_transportation_costs(inst, X, Y):
    '''Heuristic to solve CFLP by sorting facilities by their sum of transportation cost
    in ascending order, and then picking their clients as they can.

    @param  inst CFLProblem
    @param  X CFLProblem.attendance_matrix
    @param  Y CFLProblem.operating_facilities_list
    @return tuple (inst, X, Y)
    '''
    f_costs = inst.sorted_transportation()

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
