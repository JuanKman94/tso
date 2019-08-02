class CFLParameters:
    # Number of facilities
    m = -1

    # Number of clients
    n = -1

    """
    Parameters for Capacitated Facility Location Problem

    :param capacity: Fixed capacity for every plant
    :param clients: List of clients to be supplied to
    :param costs: Transportation costs matrix
    :param maintenance: List of maintenance costs for plants
    :param X: X-axis of solution matrix, if any
    :param Y: Y-axis of solution matrix, if any
    :returns: New initialized instance
    """
    def __init__(self, capacity = 1, maintenance = [], clients = [], costs = [], X = [], Y = []):
        self.capacity = capacity
        self.maintenance = maintenance
        self.clients = clients
        self.costs = costs
        self.m = len(maintenance)
        self.n = len(clients)
        self.X = X
        self.Y = Y
