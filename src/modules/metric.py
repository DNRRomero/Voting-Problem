import numpy as np
import scipy.spatial as scp
from enum import Enum

from .data_structure import Config


def density(array: np.ndarray, config: Config, single=0):
    steps, size = array.shape
    dens = lambda a, i: (1 + a[i]).sum() / (2 * size)
    return [dens(array, i) for i in range(steps)]


def energy(array: np.ndarray, config: Config, single=0):
    e = lambda x: -0.5 * (x.dot(config.adj.dot(x)))
    if single:
        return e(array) / config.edges
    steps, _ = array.shape
    return [(e(array[i])) / config.edges for i in range(steps)]


def consensus(array: np.ndarray, config: Config = None, single=0):
    c = lambda x: np.abs(x.sum())
    if single:
        return c(array)/config.size
    steps, size = array.shape
    return [c(array[i]) / size for i in range(steps)]


def hamming(array: np.ndarray, config: Config, single=0):
    steps, size = array.shape
    dist = lambda x, t: 0 if t == 0 else scp.distance.hamming(x[t], x[t - 1])
    return [dist(array, i) for i in range(steps)]


class Metric(Enum):
    Density = 1
    Energy = 2
    Hamming = 3
    Consensus = 4


def getMetrics():
    metrics = {Metric.Density: density, Metric.Energy: energy,
               Metric.Hamming: hamming, Metric.Consensus: consensus}
    return metrics
