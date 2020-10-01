from rules import *
from metric import *
from utilities import *
import scipy.spatial as scp
import pickle
import itertools


def cycleCheck(config: Config, steps, array, t):
    cycle = None
    name = '{0}_{1}_fixed_points'.format(str(config.size), str(steps))
    length = 0
    for conf in range(t):
        if scp.distance.hamming(array[conf], array[t]) == 0:
            cycle = t
            length = cycle - conf
            break
    if length == 1:
        config_file = open(name, 'ab')
        config.setStates(array[t])
        pickle.dump(config.nodes, config_file)
        config_file.close()
    return cycle


def light_evolve(t, array, steps, perm, rules, config):
    while t <= steps:
        for index in perm:
            array[t % 2] = array[(t - 1) % 2]
            state = rules[config.nodes[index].rule]((t - 1) % 2, array, config, index)
            array[t % 2][index] = state
            t += 1
    return array


def evolve(config: Config, perm: np.ndarray, steps=100, metricList=None, sequential: bool = False,
           light=False, cycleBreak=False):
    """
    :param cycleBreak:
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
    cycle = None
    if sequential and not light:
        while t <= config.size * steps:
            for index in perm:
                array[t] = array[t - 1]
                state = rules[config.nodes[index].rule](t - 1, array, config, index)
                array[t][index] = state
                t += 1
    elif light:
        array = light_evolve(t, array, steps, perm, rules, config)

    else:  # Not sequential nor light
        while t <= steps:
            array[t] = array[t - 1]
            for index in perm:
                state = rules[config.nodes[index].rule](t, array, config, index)
                array[t][index] = state
            if cycleBreak:
                cycle = cycleCheck(config, steps, array, t)
            if cycle is not None:
                break
            t += 1

    for metric in metricList:
        out[metric] = metrics[metric](array, config)
    if cycle is not None:
        # If there is a cycle, copy the metric value in cycle at the last entry
        for metric in metricList:
            out[metric][-1] = out[metric][cycle]

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
                   p_actions: List[float], labels=None, p_state=0.5):
    if labels is None:
        labels = p_actions
    state = 'p_a'
    cycles = {'length': np.zeros(samples * len(p_actions)), state: np.zeros(samples * len(p_actions))}

    prof = {state: np.zeros(samples * len(p_actions))}
    for metric in metricList:
        prof[metric.name] = np.zeros(samples * len(p_actions))

    for i, p in enumerate(p_actions):
        ring = createConfig(configType, n=n, rules=rules[i])
        for j in range(samples):
            states = [np.random.choice(a=[State.ON, State.OFF], p=[p_state, 1 - p_state]) for i in range(n)]
            ring.setStates(states)
            evol, metrics = evolve(config=ring, perm=perm, steps=steps, metricList=metricList)
            pos = i * samples + j
            cycles['length'][pos] = cycle_length(evol)
            cycles[state][pos] = labels[i]
            for e in metrics:
                prof[e.name][pos] = metrics[e][-1]
            prof[state][pos] = labels[i]

    return cycles, prof


def evolve_all_configs(n, steps: int, samples: int, perm, p_actions: List[float], metricList, labels= None):
    if labels is None:
        labels = p_actions
    cases = samples * len(p_actions)
    act_label = 'p_a'
    cycles = {'length': np.zeros(cases), act_label: np.zeros(cases)}
    prof = {act_label: np.zeros(samples * len(p_actions))}
    for metric in metricList:
        prof[metric.name] = np.zeros(cases)

    rules = [[np.random.choice(a=[Rule.STABLE, Rule.UNSTABLE], p=[p, 1 - p]) for i in range(n)] for p in p_actions]

    for i, p in enumerate(p_actions):
        ring = Ring.createRing(n, rules=rules[i])
        for j, s in enumerate(itertools.product([State.ON, State.OFF], repeat=n)):
            ring.setStates(list(s))
            evol, metrics = evolve(config=ring, perm=perm, steps=steps, metricList=metricList, cycleBreak=True)
            pos = i * samples + j
            cycles['length'][pos] = cycle_length(evol)
            cycles[act_label][pos] = labels[i]
            for e in metrics:
                prof[e.name][pos] = metrics[e][-1]
            prof[act_label][pos] = labels[i]