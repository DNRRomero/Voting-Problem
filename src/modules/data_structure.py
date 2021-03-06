from enum import IntEnum, Enum
from typing import List
from scipy import sparse


class ConfigType(Enum):
    Ring = 0
    Torus = 1
    Graph = 2


class State(IntEnum):
    ON = 1
    OFF = -1


class Rule(IntEnum):
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

    @rule.setter
    def rule(self, val):
        self._rule = val

    def __repr__(self):
        return "Node([{0}, {1}, {2}, {3}])".format(repr(self.id), repr(self.state), repr(self.rule), repr(self.degree))


class Config(object):
    def __init__(self, adj: sparse.csr_matrix, nodes, tp: ConfigType):
        self._adj = adj
        self._nodes: List[Node] = nodes
        self._size = len(nodes)
        self._type = tp
        self._edges = int(adj.sum() / 2)

    @property
    def size(self):
        return self._size

    @property
    def nodes(self):
        return self._nodes

    @property
    def adj(self):
        return self._adj

    @property
    def edges(self):
        return self._edges

    @property
    def type(self):
        return self._type

    def prod(self, array, index):
        return self.adj[index].dot(array)[0]

    def set_states(self, states: List[State]):
        assert len(states) == self.size
        for i in range(self.size):
            self.nodes[i].state = states[i]
        return self

    def set_rules(self, rules: List[Rule]):
        assert len(rules) == self.size
        for i in range(self.size):
            self.nodes[i].rule = rules[i]
        return self

    def get_states(self):
        return [node.state for node in self.nodes]

    def get_rules(self):
        return [node.rule for node in self.nodes]
