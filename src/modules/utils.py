import numpy as np
import scipy.spatial as scp
from numpy.random import default_rng

from . import Ring
from . import Torus
from .data_structure import Config, ConfigType, State, Rule
from .metric import consensus, getMetrics
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
    Returns cycle pair (length, start)
    """
    steps, _ = array.shape

    for i in range(steps):
        for j in range(i + 1, steps):
            if scp.distance.hamming(array[i], array[j]) == 0:
                return j - i, i
    return steps + 1, 0


def avg_cycle_length(array: np.ndarray, start, length):
    return np.array(consensus(array[start: start + length])).mean()


def create_config(configType: ConfigType, **kwargs):
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
    """
    returns array of states given by a magnetization value mag, where
    0.5 +mag/2 arrays cells are of type pref1 and the rest is of type pref2
    """
    rng = default_rng()
    d = 1 if pref == State.ON else -1
    if mag < 0:
        mag = abs(mag)
        d = -d
    states = [State.ON] * round((size * (0.5 + d * mag / 2)) - 10 ** (-9)) + [State.OFF] * round(
        (size * (0.5 - d * mag / 2) + 10 ** (-9)))
    rng.shuffle(states)
    return states


def states_against_stiff(config: Config, stiff_type, mag, pref):
    for node in config.nodes:
        if node.rule == Rule.STIFF:
            node.state = stiff_type
    non_stiff = list(filter(lambda y: y.rule != Rule.STIFF, config.nodes))
    states = states_per_magnet(len(non_stiff), mag, pref)
    for i, node in enumerate(non_stiff):
        node.state = states[i]
    return config


def size_round(size, fct):
    """
    Returns the integer fraction (fct, 1-fct) of a certain integer size
    """
    return round(size * (fct + 10 ** (-9))), round(size * (1 - fct - 10 ** (-9)))


def rules_per_factor(size, fct, pref1=Rule.STABLE, pref2=Rule.UNSTABLE):
    """
    returns array of majority rules given by an fct fraction
    of array cells of type pref1 and (1-fct) cells of type pref2
    """
    rng = default_rng()
    size1, size2 = size_round(size, fct)
    rules = [pref1] * size1 + [pref2] * size2
    rng.shuffle(rules)
    return rules


def rules_per_freeze_and_factor(size, freeze_fct, pref_fct, pref1=Rule.STABLE, pref2=Rule.UNSTABLE):
    """
    returns array of majority rules given by a freeze_fct fraction of array cells
    set to be freezing and a pref_fct*(1-freeze_fct) fraction is set to be of type pref1
    while the rest is of type pref2
    """
    rng = default_rng()
    freeze_sz1, freeze_sz2 = size_round(size, freeze_fct)
    pref_sz1, pref_sz2 = size_round(freeze_sz2, pref_fct)
    rules = [Rule.STIFF] * freeze_sz1 \
            + [pref1] * pref_sz1 \
            + [pref2] * pref_sz2
    rng.shuffle(rules)
    return rules
