from enum import IntEnum, Enum
from typing import List


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
    def __init__(self, ID, state, rule):
        self._id = ID
        self._state = state
        self._rule = rule

    @property
    def rule(self):
        return self._rule

    @property
    def id(self):
        return self._id

    @property
    def state(self):
        return self._state


class Config(object):
    def __init__(self, adj, nodes):
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
