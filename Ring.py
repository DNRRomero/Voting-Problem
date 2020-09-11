import numpy as np
from data_structure import *


# def setStates(rand = True):
# def setRules(rand= True):

def createRing(n, p_action, p_state, action1=Action.STABLE, action2=Action.UNSTABLE):
    nodes = [Node(i, np.random.choice(a=[State.ON, State.OFF], p=[p_state, 1 - p_state]),
                  np.random.choice(a=[action1, action2], p=[p_action, 1 - p_action]), 2) for i in range(n)]

    cols = np.array([[(i - 1) % n, (i + 1) % n] for i in range(n)]).reshape(1, 2 * n)[0]

    rows = np.array([i // 2 for i in range(2 * n)])
    val = np.ones(2 * n, dtype=int)
    mat = sparse.coo_matrix((val, (rows, cols)))
    adj = mat.tocsr()

    ring = Config(adj, nodes)

    return ring
