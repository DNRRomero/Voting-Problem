import numpy as np
from data_structure import *


# def setStates(rand = True):
# def setRules(rand= True):

def createRing(n, p_action=0.5, p_state=0.5, states=None, rules=None, action1=Rule.STABLE, action2=Rule.UNSTABLE):
    _state = lambda i: np.random.choice(a=[State.ON, State.OFF], p=[p_state, 1 - p_state]) if states is None else \
        states[i]
    _rule = lambda i: np.random.choice(a=[action1, action2], p=[p_action, 1 - p_action]) if rules is None else rules[i]
    nodes = [Node(i, _state(i), _rule(i), 2) for i in range(n)]

    cols = np.array([[(i - 1) % n, (i + 1) % n] for i in range(n)]).reshape(1, 2 * n)[0]

    rows = np.array([i // 2 for i in range(2 * n)])
    val = np.ones(2 * n, dtype=int)
    mat = sparse.coo_matrix((val, (rows, cols)))
    adj = mat.tocsr()

    ring = Config(adj, nodes, type=ConfigType.Ring)

    return ring
