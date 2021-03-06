import numpy as np
from typing import List
import scipy.spatial as scp
import pickle
import itertools
import pandas as pd

from .utils import setup, create_config, cycle_length
from .data_structure import Rule, State, ConfigType, Config


def save_fixed_point(config: Config, steps, array, t):
    name = '{0}_{1}_{2}_fixed_points.txt'.format(config.type.name, str(config.size), str(steps))
    config_file = open(name, 'ab')
    config.set_states(array[t])
    pickle.dump(config.nodes, config_file)
    config_file.close()


def order_update(array, config, perm, rules):
    """
    Updates the current array cells of a configuration according to a fixed order
    """
    for index in perm:
        array[index] = rules[config.nodes[index].rule](array, config, index)
    return array


def par_update(array, config, rules):
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
    if length == 1 and fixedPoints:
        save_fixed_point(config, steps, array, t)

    return cycle, length


def light_evolve(t, array, steps, perm, rules, config):
    while t <= steps:
        for index in perm:
            array[t % 2] = array[(t - 1) % 2]
            state = rules[config.nodes[index].rule]((t - 1) % 2, array, config, index)
            array[t % 2][index] = state
            t += 1
    return array



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


def evolve(config: Config, perm: np.ndarray, steps=100, metricList=None, light=False,
           cycleBreak=True):
    if metricList is None:
        metricList = []
    rules, metrics = setup()
    out = {}
    t_steps = 2 if light else steps + 1
    array = np.zeros((t_steps, config.size), dtype=np.int8)
    array[0] = np.array([a.state for a in config.nodes])

    t = 1
    cycle, length = False, None
    if light:
        array = light_evolve(t, array, steps, perm, rules, config)
    else:  # regular
        while t <= steps and cycle:
            array[t] = order_update(array[t - 1].copy(), config, perm, rules)
            if cycleBreak:
                # cycle, length = cycleCheck(config, steps, array, t)
                cycle = is_cycle(array, t)
            t += 1

    for metric in metricList:
        out[metric] = metrics[metric](array, config)
    if cycle:
        # If there is a cycle, copy the average metric value in cycle at the last entry
        cycle, length = cycleCheck(config, steps, array, t)
        for metric in metricList:
            out[metric][-1] = np.mean(out[metric][cycle: cycle + length])

    return array, out


def multi_evolve(configs: List[Config], perm: np.ndarray, steps=100, metricList=None):
    out = {}
    for config in configs:
        _, metrics = evolve(config, perm, steps, metricList, light=False)
        for metric in metrics:
            if metric in out:
                out[metric].append(metrics[metric])
            else:
                out[metric] = [metrics[metric]]

    return out


def config_sampler(configType: ConfigType, n, steps, perm, rules, metricList, samples: int,
                   p_actions: List[float], labels=None, p_state=0.5, size=None, **kwargs):
    if labels is None:
        labels = p_actions
    if size is None:
        size = n
    state = '$p_{stable}$'
    cases = samples * len(p_actions)
    data = {'length': np.zeros(cases), state: np.zeros(cases, dtype='<U20')}
    for metric in metricList:
        data[metric.name] = np.zeros(samples * len(p_actions))
    conf = create_config(configType, n=n, **kwargs)
    for j in range(samples):
        if j % 100 == 0:
            print(j)
        states = np.random.choice(a=[State.ON, State.OFF], size=size, p=[p_state, 1 - p_state])
        conf.set_states(states)
        for i, p in enumerate(p_actions):
            conf.set_rules(rules[i])
            evol, metrics = evolve(config=conf, perm=perm, steps=steps, metricList=metricList, cycleBreak=True)
            pos = i * samples + j
            data['length'][pos] = cycle_length(evol)[0]
            data[state][pos] = labels[i]
            for e in metrics:
                data[e.name][pos] = metrics[e][-1]
    datum = pd.DataFrame(data)
    return datum


def evolve_all_configs(n, steps: int, samples: int, perm, p_actions: List[float], metricList,
                       size=None, labels=None, configType: ConfigType = ConfigType.Ring, **kwargs):
    if labels is None:
        labels = p_actions
    if size is None:
        size = n
    cases = samples * len(p_actions)
    act_label = '$p_{stable}$'
    data = {'length': np.zeros(cases), act_label: np.zeros(cases, dtype='<U30')}
    for metric in metricList:
        data[metric.name] = np.zeros(cases)

    rules = [np.random.choice(a=[Rule.STABLE, Rule.UNSTABLE], size=size, p=[p, 1 - p]) for p in p_actions]
    for i, p in enumerate(p_actions):
        print(i)
        conf = create_config(configType, n=n, rules=rules[i], **kwargs)
        for j, s in enumerate(itertools.product([State.ON, State.OFF], repeat=size)):
            conf.set_states(list(s))
            evol, metrics = evolve(config=conf, perm=perm, steps=steps, metricList=metricList, cycleBreak=True)
            pos = i * samples + j
            data['length'][pos] = cycle_length(evol)[0]
            data[act_label][pos] = labels[i]
            for e in metrics:
                data[e.name][pos] = metrics[e][-1]
            data[act_label][pos] = labels[i]
    datum = pd.DataFrame(data)

    return datum
