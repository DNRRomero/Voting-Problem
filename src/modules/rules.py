import numpy as np
from .data_structure import Config, Rule


def stableMajority(array: np.ndarray, config: Config, index):
    even = 1 if config.nodes[index].degree % 2 == 0 else 0
    state = 1 if config.prod(array, index) + even*array[index] > 0 else -1
    return state


def unstableMajority(array, config: Config, index):
    even = 1 if config.nodes[index].degree % 2 == 0 else 0
    state = 1 if config.prod(array, index) - even*array[index] > 0 else -1
    return state


def oneBiased(array, config: Config, index):
    state = 1 if config.prod(array, index) >= 0 else -1
    return state


def zeroBiased(array, config: Config, index):
    state = 1 if config.prod(array, index) > 0 else -1
    return state


def stiff(array, config: Config, index):
    return array[index]


def getRules():
    rules = {Rule.STABLE: stableMajority, Rule.UNSTABLE: unstableMajority, Rule.ONE_BIASED: oneBiased,
             Rule.ZERO_BIASED: zeroBiased, Rule.STIFF: stiff}
    return rules
