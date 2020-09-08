from data_structure import *
import numpy as np


def density(array: np.ndarray, config: Config):
    return [np.bincount[array[i]] for i in range(len(array))]


class Metric(Enum):
    EV = 0
    DENSITY = 1


def getMetrics():
    metrics = {Metric.DENSITY: density}
    return metrics
