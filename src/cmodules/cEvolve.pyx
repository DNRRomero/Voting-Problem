from cython.view cimport array as cvarray
from cython cimport boundscheck, wraparound
import numpy as np
import scipy.spatial as scp
import itertools

from modules.utils import setup
from modules.data_structure import Config



def par_update(array, config, rules):
    # Esto puede acelerarse fácilmente mediante vectorización, se necesita
    # 1. definir la función no lineal que entrega la matriz de reglas, 2. implementar en numpy
    a = np.empty_like(array)
    for index in range(len(config.nodes)):
        a[index] = rules[config.nodes[index].rule](array, config, index)
    return a


def is_cycle(array, t):
    return len(array) != len(np.unique(array[0:t + 1], axis=0))


def cycleCheck(config: Config, steps, array, t, fixedPoints=False):
    cycle = None
    length = 0
    for start in range(t):
        if scp.distance.hamming(array[start], array[t]) == 0:
            cycle = start
            length = t - start
            break
    return cycle, length




def parallel_evolve(config: Config, steps=100, metricList=None, cycleBreak=True):
    if metricList is None:
        metricList = []
    rules, metrics = setup()
    out = {}
    t_steps = steps + 1
    array = np.zeros((t_steps, config.size), dtype=np.int8)
    for index in range(config.size):
        array[0][index] = config.nodes[index].state
    t = 1
    cycle, length = None, None
    while t <= steps and cycle is None:
        array[t] = par_update(array[t - 1], config, rules)
        if cycleBreak:
            cycle, length = cycleCheck(config, steps, array, t)
        t += 1

    for metric in metricList:
        out[metric] = metrics[metric](array, config)
    if cycle is not None:
        # If there is a cycle, copy the average metric value in cycle at the last entry
        for metric in metricList:
            out[metric][-1] = np.mean(out[metric][cycle: cycle + length])

    return array, out

@boundscheck(False)
@wraparound(False)
def evolve(config: Config, perm: np.ndarray, steps=100, metricList=None, cycleBreak=True):
    if metricList is None:
        metricList = []
    rules, metrics = setup()
    cdef int[:] perm_view = perm
    cdef int size = config.size
    cdef int t_steps = steps + 1
    cdef int length
    cdef int t, i;
    cdef int[:, ::1] array = np.zeros((t_steps, size), dtype=np.int8)
    array[0] = np.array([a.state for a in config.nodes])
    cycle = False
    out = {}

    for t in range(1, t_steps):
        for i in range(size):
            array[t, perm_view[i]] = rules[config.nodes[perm_view[i]].rule](array, config, perm_view[i])
        if cycleBreak:
            cycle = is_cycle(array, t)
            if cycle:
                break

    for metric in metricList:
        out[metric] = metrics[metric](array, config)
    if cycle:
        # If there is a cycle, copy the average metric value in cycle at the last entry
        cycle, length = cycleCheck(config, steps, array, t)
        for metric in metricList:
            out[metric][t_steps] = np.mean(out[metric][cycle: cycle + length])

    return array, out
