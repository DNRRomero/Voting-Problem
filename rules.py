import numpy as np
from data_structure import *


def stableMajority(t, array: np.ndarray, config: Config, index):
    even = 1 if config.nodes[index].degree % 2 == 0 else 0
    state = 1 if config.prod(t, array, index) + even*array[t][index] > 0 else -1
    return state


def unstableMajority(t, array, config: Config, index):
    even = 1 if config.nodes[index].degree % 2 == 0 else 0
    state = 1 if config.prod(t, array, index) - even*array[t][index] > 0 else -1
    return state


def oneBiased(t, array, config: Config, index):
    state = 1 if config.prod(t, array, index) >= 0 else -1

    return state


def zeroBiased(t, array, config: Config, index):
    state = 1 if config.prod(t, array, index) > 0 else -1
    return state


def stiff(t, array, config: Config, index):
    return array[t][index]


def getRules():
    rules = {Action.STABLE: stableMajority, Action.UNSTABLE: unstableMajority, Action.ONE_BIASED: oneBiased,
             Action.ZERO_BIASED: zeroBiased, Action.STIFF: stiff}
    return rules
