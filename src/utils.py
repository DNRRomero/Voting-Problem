import numpy as np
import scipy.spatial as scp

import Ring
import Torus
from data_structure import ConfigType
from metric import magnetization, getMetrics
from rules import getRules


def primes_up_to(n):
    # https://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
    """ Returns a array of primes, p < n """
    assert n >= 2
    sieve = np.ones(n // 2, dtype=np.bool)
    for i in range(3, int(n ** 0.5) + 1, 2):
        if sieve[i // 2]:
            sieve[i * i // 2::i] = False
    return np.r_[2, 2 * np.nonzero(sieve)[0][1::] + 1]


def cycle_length(array: np.ndarray):
    """
    :return: returns cycle pair (length, start)
    """
    steps, _ = array.shape

    for i in range(steps):
        for j in range(i + 1, steps):
            if scp.distance.hamming(array[i], array[j]) == 0:
                return j - i, i
    return steps + 1, 0


def avg_cycle_length(array: np.ndarray, start, length):
    return np.array(magnetization(array[start: start + length])).mean()


def createConfig(configType: ConfigType, **kwargs):
    switcher = {
        ConfigType.Ring:
            Ring.createRing,
        ConfigType.Torus:
            Torus.createTorus
        # ConfigType.Graph:

    }
    func = switcher.get(configType, lambda: "invalid")
    return func(**kwargs)


def setup():
    return getRules(), getMetrics()
