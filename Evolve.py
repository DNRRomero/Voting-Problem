from rules import *
from metric import *
from utilities import *


def evolve(config: Config, perm: np.ndarray, steps=100, metricList=None, sequential: bool = False, light=False):
    """
    :param light:
    :param sequential:
    :param config:
    :param perm:
    :param steps:
    :param metricList:
    :return:
    """
    if metricList is None:
        metricList = []
    rules = getRules()
    metrics = getMetrics()
    out = {}
    seq = config.size if sequential else 1
    size = 2 if light else steps * seq + 1
    array = np.zeros((size, config.size), dtype=np.int8)
    for index in range(config.size):
        array[0][index] = config.nodes[index].state
    t = 1
    if sequential and not light:
        while t <= config.size * steps:
            for index in perm:
                array[t] = array[t - 1]
                state = rules[config.nodes[index].rule](t - 1, array, config, index)
                array[t][index] = state
                t += 1
    elif light:
        while t <= steps:
            for index in perm:
                array[t % 2] = array[(t - 1) % 2]
                state = rules[config.nodes[index].rule]((t - 1) % 2, array, config, index)
                array[t % 2][index] = state
                t += 1
    else:
        while t <= steps:
            array[t] = array[t - 1]
            for index in perm:
                state = rules[config.nodes[index].rule](t, array, config, index)
                array[t][index] = state
            t += 1

    for metric in metricList:
        out[metric] = metrics[metric](array, config)

    return array, out


def multi_evolve(configs: List[Config], perm: np.ndarray, steps=100, metricList=None, sequential: bool = False):
    out = {}
    for config in configs:
        _, metrics = evolve(config, perm, steps, metricList, sequential, light=False)
        for metric in metrics:
            if metric in out:
                out[metric].append(metrics[metric])
            else:
                out[metric] = [metrics[metric]]

    return out


def config_sampler(configType: ConfigType, n, steps, perm, rules, metricList, samples: int,
                   p_actions: List[float], p_state=0.5):
    state = 'p_a'
    cycles = {'length': np.zeros(samples * len(p_actions)), state: np.zeros(samples * len(p_actions))}

    prof = {state: np.zeros(samples * len(p_actions))}
    for metric in metricList:
        prof[metric] = np.zeros(samples * len(p_actions))

    for i, p in enumerate(p_actions):
        ring = createConfig(configType, size=n, rules=rules[i])
        for j in range(samples):
            states = [np.random.choice(a=[State.ON, State.OFF], p=[p_state, 1 - p_state]) for i in range(n)]
            ring.setStates(states)
            evol, metrics = evolve(config=ring, perm=perm, steps=steps, metricList=metricList)
            pos = i * samples + j
            cycles['length'][pos] = cycle_length(evol)
            cycles[state][pos] = p_actions[i]
            for e in metrics:
                prof[e][pos] = metrics[e][-1]
            prof[state][pos] = p_actions[i]
