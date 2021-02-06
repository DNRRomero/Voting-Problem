import numpy as np
import scipy.spatial as scp
from enum import Enum

from .data_structure import Config


def density(array: np.ndarray, config: Config, single=0):
    dens = lambda a: (1 + a).sum(axis=1-single) / (2 * config.size)
    return dens(array)


def energy(array: np.ndarray, config: Config, single=0):
    if single:
        return -0.5 * (array.dot(config.adj.dot(array))) / config.edges
    return -0.5*np.einsum('ij,ij->i', array, array@config.adj.T)/config.edges


def consensus(array: np.ndarray, config: Config = None, single=0):
    return np.abs(array.sum(axis=1-single))/config.size
    # c = lambda x: np.abs(x.sum())
    # if single:
    #     return c(array)/config.size
    # steps, size = array.shape
    # return [c(array[i]) / size for i in range(steps)]


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
