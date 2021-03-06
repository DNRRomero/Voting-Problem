import numpy as np
from scipy import sparse
from numpy.random import default_rng

from .data_structure import Neighborhood, Config, ConfigType, Rule, Node, State


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


def createTorus(n: int, m: int = None, p_action=0.5, p_state=0.5, states=None, rules=None,
                neighs=Neighborhood.NEUMANN, action1=Rule.STABLE, action2=Rule.UNSTABLE):
    """

    :param rules:
    :param states:
    :param n: number of rows
    :param m: number of columns
    :param p_action: probability for assigning two actions
    :param p_state: probability of state assignment
    :param neighs: type of neighborhood (Moore or Neumann)
    :param action1: action 1
    :param action2: action 2
    :return: a Config object containing an adjacency matrix and a node profile
    """
    rng = default_rng()
    deg = 4 if neighs == Neighborhood.NEUMANN else 8
    if m is None:
        m = n
    _state = lambda i: rng.choice(a=[State.ON, State.OFF], p=[p_state, 1 - p_state]) \
        if states is None else states[i]
    _rule = lambda i: rng.choice(a=[action1, action2], p=[p_action, 1 - p_action]) \
        if rules is None else rules[i]
    nodes = [Node(i, _state(i), _rule(i), deg) for i in range(n * m)]

    adj = set_adjacency(n, m, deg, neighs)

    torus = Config(adj, nodes, tp=ConfigType.Torus)

    return torus
