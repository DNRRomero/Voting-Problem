import numpy as np
from data_structure import *
from scipy import sparse


def set_adjacency(n, m, deg, neighs):
    pair = lambda k: (k // m, k % m)
    single = lambda i, j: i * m + j

    if neighs == Neighborhood.NEUMANN:
        cols = np.array([
            [single((pair(i)[0] + 1) % n, pair(i)[1]),
             single((pair(i)[0] - 1) % n, pair(i)[1]),
             single(pair(i)[0], (pair(i)[1] + 1) % m),
             single(pair(i)[0], (pair(i)[1] - 1) % m)] for i in range(n * m)]).reshape(1, deg * n * m)[0]
    else:
        cols = np.array([
            [single((pair(i)[0] + 1) % n, pair(i)[1]),
             single((pair(i)[0] - 1) % n, pair(i)[1]),
             single(pair(i)[0], (pair(i)[1] + 1) % m),
             single(pair(i)[0], (pair(i)[1] - 1) % m),
             single((pair(i)[0] + 1) % n, (pair(i)[1] + 1) % m),
             single((pair(i)[0] + 1) % n, (pair(i)[1] - 1) % m),
             single((pair(i)[0] - 1) % n, (pair(i)[1] + 1) % m),
             single((pair(i)[0] - 1) % n, (pair(i)[1] - 1) % m)] for i in range(n * m)]).reshape(1, deg * n * m)[0]
    rows = np.array([i // deg for i in range(deg * n * m)])
    val = np.ones(deg * n * m, dtype=int)
    mat = sparse.coo_matrix((val, (rows, cols)))
    adj = mat.tocsr()
    return adj


def createTorus(n: int, m: int, p_action=0.5, p_state=0.5, neighs=Neighborhood.NEUMANN, action1=Action.STABLE,
                action2=Action.UNSTABLE):
    """

    :param n: number of rows
    :param m: number of columns
    :param p_action: probability for asigning two actions
    :param p_state: probability of state assignment
    :param neighs: type of neighborhood (Moore or Neumann)
    :param action1: action 1
    :param action2: action 2
    :return: a Config object containing an adjacency matrix and a node profile
    """
    deg = 4 if neighs == Neighborhood.NEUMANN else 8
    nodes = [Node(i, np.random.choice(a=[State.ON, State.OFF], p=[p_state, 1 - p_state]),
                  np.random.choice(a=[action1, action2], p=[p_action, 1 - p_action]), deg) for i in range(n * m)]

    adj = set_adjacency(n, m, deg, neighs)

    torus = Config(adj, nodes)

    return torus
