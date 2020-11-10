import numpy as np
import scipy.spatial as scp

from . import Ring
from . import Torus
from .data_structure import ConfigType, State, Rule
from .metric import magnetization, getMetrics
from .rules import getRules


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


def states_per_magnet(size, mag, pref=State.ON):
    d = 1 if pref == State.ON else -1
    states = [State.ON] * round((size * (0.5 + d*mag / 2)) - 10 ** (-9)) + [State.OFF] * round(
        (size * (0.5 - d*mag / 2) + 10 ** (-9)))
    np.random.seed()
    np.random.shuffle(states)
    return states

def rules_per_factor(size, fct, pref= Rule.STABLE):
    d = 1 if pref == Rule.STABLE else -1
    rules = [Rule.STABLE] * round((size * (0.5 + d*fct / 2)) - 10 ** (-9)) + [Rule.UNSTABLE] * round(
        (size * (0.5 - d*fct / 2) + 10 ** (-9)))
    np.random.seed()
    np.random.shuffle(rules)
    return rules
