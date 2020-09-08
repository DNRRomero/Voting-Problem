from rules import *
from metric import *


def evolve(config: Config, perm: np.ndarray, steps=100, metricList=None):
    if metricList is None:
        metricList = []
    rules = getRules()
    metrics = getMetrics()
    out = {}
    array = np.zeros((steps + 1, config.size))
    for index in range(config.size):
        array[0][index] = config.nodes[index].state
    t = 1
    while t <= steps:
        for index in perm:
            state = rules[config.nodes[index].rule](t - 1, array, config, index)
            array[t][index] = state
        t += 1

    for metric in metricList:
        out[Metric.metric] = metrics[metric](array, config)

    out[Metric.EV] = array
    return out
