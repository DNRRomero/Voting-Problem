import numpy as np
from .data_structure import Node, Config, ConfigType
from scipy import sparse
from enum import Enum, IntEnum
from typing import List
from itertools import chain, product


class Part(IntEnum):
    LEFT = 0
    RIGHT = 1


class PartitionNode(Node):
    def __init__(self, ID, state, rule, deg, part: Part, comp=-1):
        super(Node, self).__init__(ID, state, rule, deg)
        self.part = part
        self.comp = comp
        self.util = 0
        self.to_nuls = 0
        self.neighs = set()

    def isC1(self):
        pass

    def isC2(self):
        pass

    def is_pivot(self):
        return next((True for y in 0))


def adj(x, y):
    pass


class Partition(Config):

    def __init__(self, adj: sparse.csr_matrix, nodes: List[PartitionNode], tp: ConfigType, left, right):
        super(Config, self).__init__(adj, nodes, tp)
        self.sides = {Part.LEFT: left, Part.RIGHT: right}
        self.nice = False
        self.nuls = {Part.LEFT: 0, Part.RIGHT: 0}

    def left(self):
        return self.sides[Part.LEFT]

    def right(self):
        return self.sides[Part.RIGHT]

    def set_neighbors(self):
        for i,v in enumerate(self.nodes):
            v.neighs

    def is_p1(self):
        minor = False
        adjf = lambda x, y: 1 if adj(x, y) else 0
        pivot = next((False for x, y in product(self.left, self.right) if
                      self.nodes[x].util + self.nodes[y].util > -2 * adjf(x, y)), True)
        for side in self.sides.values():
            if len(side) <= self.size // 2 and next((True for x in self.nodes if x.util > 0), False):
                minor = True
        return pivot & minor

    def is_p2(self):
        negs = lambda x: (sum(1 for y in self.left() if adj(x, y) and y.util < 0) > (x.util + 2) // 2) and x.util > 0
        negx = next((False for x in self.nodes if negs(x)), True)
        nul = False
        for i, side in enumerate(self.sides.values()):
            if self.nuls[(i + 1) % 2] == 0 and len(side) <= self.size // 2 and True:
                nul = True
        return negx and nul

    def is_p3(self):
        adjf = lambda x, y: 1 if adj(x, y) else 0
        pivot = next((False for x, y in product(self.left, self.right) if
                      self.nodes[x].util + self.nodes[y].util > -2 * adjf(x, y)), True)
        util = next((False for x in self.nodes if x.util > 0), True)

        return util and pivot

    def is_nice(self):
        return self.is_p1() | self.is_p2() | self.is_p3()

    def any_pivot_agent(self):
        return next((True for n in self.left() if self.nodes[n].is_pivot()), False)

    def get_base_set(self, node_id):
        node= self.nodes[node_id]
        self.sides[node.part]
        pass

    def get_dual_set(self, node_id):
        pass
    def removeC1(self, node_id):
        base = self.nodes[node_id].base_set()
        dual = self.nodes[node_id].dual_set()
        for d in dual:
            self.change_side(d)
        for b in chain(base, node_id):
            self.change_side(b)
        pass

    def removeC2(self, node_id):
        path = []
        le = len(path)
        for i in range(le - 1):
            pass
        pass

    def change_side(self, node_id):
        side = self.nodes[node_id].part
        self.sides[side].discard(node_id)
        self.sides[(side + 1) % 2].add(node_id)
        self.nodes[node_id].part = (side + 1) % 2

    def swap(self, left_node, right_node):
        self.change_side(left_node)
        self.change_side(right_node)
