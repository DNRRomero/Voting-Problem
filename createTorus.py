import numpy as np
from data_structure import *


def createTorus(n, m, p_action=0.5, p_state=0.5, neighs=Neighborhood.NEUMANN, action1=Action.STABLE,
                action2=Action.UNSTABLE):
    nodes = [Node(i, np.random.choice(a=[State.ON, State.OFF], p=[p_state, 1 - p_state]),
                  np.random.choice(a=[action1, action2], p=[p_action, 1 - p_action])) for i in range(n * m)]
    adj = np.zeros((n * m, n * m))
    pair = lambda k: (k // m, k % m)
    single = lambda i, j: i * m + j
    for i in range(n):
        x = pair(i)[0]
        y = pair(i)[1]
        adj[i][single(x + 1 % n, y)] = 1
        adj[i][single(x - 1 % n, y)] = 1
        adj[i][single(x, y + 1 % m)] = 1
        adj[i][single(x, y - 1 % m)] = 1
        if neighs == Neighborhood.MOORE:
            adj[i][single(x + 1 % n, y + 1 % m)] = 1
            adj[i][single(x + 1 % n, y - 1 % m)] = 1
            adj[i][single(x - 1 % n, y + 1 % m)] = 1
            adj[i][single(x - 1 % n, y - 1 % m)] = 1

    torus = Config(adj, nodes)

    return torus

# def setStates(rand = True):
# def setRules(rand= True):
