from data_structure import *
import numpy as np
import scipy.spatial as scp


def density(array: np.ndarray, config: Config):
    steps, size = array.shape
    return [(1+array[i]).sum()/(2*size) for i in range(steps)]


def spinGlass(array: np.ndarray, config: Config):
    steps, size = array.shape
    b = np.array([node.degree / 2 + (0.5 if node.rule == Rule.STABLE else 0) for node in config.nodes])
    energy = lambda x: -0.5*(x.dot(config.adj.dot(x))) + x.dot(b)
    return [energy((array[i]+1)/2) for i in range(steps)]


def hamming(array: np.ndarray, config: Config):
    steps, size = array.shape
    dist = lambda x, t: 0 if t == 0 else scp.distance.hamming(x[t], x[t-1])
    return [dist(array, i) for i in range(steps)]


class Metric(Enum):
    Density = 1
    SpinGlass = 2
    Hamming = 3


def getMetrics():
    metrics = {Metric.Density: density, Metric.SpinGlass: spinGlass, Metric.Hamming: hamming}
    return metrics
