from enum import IntEnum, Enum
from typing import List
from scipy import sparse


class State(IntEnum):
    ON = 1
    OFF = -1


class Action(Enum):
    STABLE = 0
    UNSTABLE = 1
    ONE_BIASED = 2
    ZERO_BIASED = 3
    STIFF = 4


class Neighborhood(Enum):
    NEUMANN = 0
    MOORE = 1


class Node(object):
    def __init__(self, ID, state, rule, deg):
        self._id = ID
        self._state = state
        self._rule = rule
        self.degree = deg

    @property
    def rule(self):
        return self._rule

    @rule.setter
    def rule(self, val):
        self._rule = val

    @property
    def id(self):
        return self._id

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val):
        self._state = val


class Config(object):
    def __init__(self, adj: sparse.csr_matrix, nodes):
        self._adj = adj
        self._nodes: List[Node] = nodes
        self._size = len(nodes)

    @property
    def size(self):
        return self._size

    @property
    def nodes(self):
        return self._nodes

    @property
    def adj(self):
        return self._adj

    def prod(self, t, array, index):
        return self.adj[index].dot(array[t])[0]

    def setStates(self, states: List[State]):
        assert len(states) == self.size
        for i in range(self.size):
            self.nodes[i].state = states[i]

    def setRules(self, rules: List[Action]):
        assert len(rules) == self.size
        for i in range(self.size):
            self.nodes[i].rule = rules[i]
