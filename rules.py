import numpy as np
from data_structure import *


def stableMajority(t, array: np.ndarray, config: Config, index):
    state = 1 if np.dot(config.adj[index], array[t]) + array[t][index] > 0 else -1
    return state


def unstableMajority(t, array, config: Config, index):
    state = 1 if np.dot(config.adj[index], array[t]) - array[t][index] < 0 else -1
    return state


def oneBiased(t, array, config: Config, index):
    state = 1 if np.dot(config.adj[index], array[t]) >= 0 else -1

    return state


def zeroBiased(t, array, config: Config, index):
    state = 1 if np.dot(config.adj[index], array[t]) > 0 else -1
    return state


def stiff(t, array, config: Config, index):
    return array[t][index]


def getRules():
    rules = {Action.STABLE: unstableMajority, Action.UNSTABLE: unstableMajority, Action.ONE_BIASED: oneBiased,
             Action.ZERO_BIASED: zeroBiased, Action.STIFF: stiff}
    return rules
