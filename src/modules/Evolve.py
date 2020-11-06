import numpy as np
from typing import List
import scipy.spatial as scp
import pickle
import itertools
import pandas as pd

from .utils import setup, createConfig, cycle_length
from .data_structure import Rule, State, ConfigType, Config


def cycleCheck(config: Config, steps, array, t, fixedPoints=False):
    cycle = None
    name = '{0}_{1}_{2}_fixed_points.txt'.format(config.type.name, str(config.size), str(steps))
    length = 0
    for start in range(t):
        if scp.distance.hamming(array[start], array[t]) == 0:
            cycle = start
            length = t - start
            break
    if length == 1 and fixedPoints:
        config_file = open(name, 'ab')
        config.set_states(array[t])
        pickle.dump(config.nodes, config_file)
        config_file.close()
    return cycle, length


def light_evolve(t, array, steps, perm, rules, config):
    while t <= steps:
        for index in perm:
            array[t % 2] = array[(t - 1) % 2]
            state = rules[config.nodes[index].rule]((t - 1) % 2, array, config, index)
            array[t % 2][index] = state
            t += 1
    return array


def sequential_evolve(t, array, steps, perm, rules, config):
    while t <= config.size * steps:
        for index in perm:
            array[t] = array[t - 1]
            state = rules[config.nodes[index].rule](t - 1, array, config, index)
            array[t][index] = state
            t += 1
    return array


def evolve(config: Config, perm: np.ndarray, steps=100, metricList=None, sequential: bool = False,
           light=False, cycleBreak=False, fixedPoints=False):
    if metricList is None:
        metricList = []
    rules, metrics = setup()
    out = {}
    seq = config.size if sequential else 1
    size = 2 if light else steps * seq + 1
    array = np.zeros((size, config.size), dtype=np.int8)
    for index in range(config.size):
        array[0][index] = config.nodes[index].state
    t = 1
    cycle = None
    length = None
    if sequential and not light:
        array = sequential_evolve(t, array, steps, perm, rules, config)
    elif light:
        array = light_evolve(t, array, steps, perm, rules, config)

    else:  # Not sequential nor light
        while t <= steps:
            array[t] = array[t - 1]
            for index in perm:
                state = rules[config.nodes[index].rule](t, array, config, index)
                array[t][index] = state
            if cycleBreak:
                cycle, length = cycleCheck(config, steps, array, t, fixedPoints=fixedPoints)
            if cycle is not None:
                break
            t += 1

    for metric in metricList:
        out[metric] = metrics[metric](array, config)
    if cycle is not None:
        # If there is a cycle, copy the average metric value in cycle at the last entry
        for metric in metricList:
            out[metric][-1] = np.mean(out[metric][cycle: cycle + length])

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
    conf = createConfig(configType, n=n, **kwargs)
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
        conf = createConfig(configType, n=n, rules=rules[i], **kwargs)
        for j, s in enumerate(itertools.product([State.ON, State.OFF], repeat=size)):
            conf.set_states(list(s))
            evol, metrics = evolve(config=conf, perm=perm, steps=steps, metricList=metricList, cycleBreak=True,
                                   fixedPoints=True)
            pos = i * samples + j
            data['length'][pos] = cycle_length(evol)[0]
            data[act_label][pos] = labels[i]
            for e in metrics:
                data[e.name][pos] = metrics[e][-1]
            data[act_label][pos] = labels[i]
    datum = pd.DataFrame(data)

    return datum
