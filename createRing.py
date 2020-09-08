import numpy as np
from data_structure import *


# def setStates(rand = True):
# def setRules(rand= True):

def createRing(n, p_action, p_state, action1=Action.STABLE, action2=Action.UNSTABLE):
    nodes = [Node(i, np.random.choice(a=[State.ON, State.OFF], p=[p_state, 1 - p_state]),
                  np.random.choice(a=[action1, action2], p=[p_action, 1 - p_action])) for i in range(n)]
    adj = np.zeros((n, n))
    for i in range(n):
        adj[i][i - 1 % n] = 1
        adj[i][i + 1 % n] = 1
    ring = Config(adj, nodes)

    return ring
