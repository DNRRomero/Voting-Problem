import numpy as np
import pandas as pd
import json
import sys

from Evolve import evolve
from data_structure import ConfigType, Rule, State
from metric import Metric
from utils import createConfig, cycle_length

# values = json.load(sys.stdin.read(n=1))
# arg = sys.argv
# n = int(arg[1])
# steps = int(arg[2])
n = 256
steps = 2500
#seed = 654798203
seed = None
stab_range = 'fixed'
size = n
c_type = ConfigType.Ring
p_state = 0.5

p_actions = None
labels = None
if stab_range == 'var':
    p_actions = [0, 1 / np.power(size, 2), 1 / np.power(size, 1.5), 1 / size, 1 / np.sqrt(size),
                 1 / np.power(size, 1 / 3),
                 1 / np.power(np.log2(size), 2), 1 / np.log2(size)]
    labels = [r'$0$', r'$1/n^2$', r'$1/n^{3/2}$', r'$1/n$', r'$1/\sqrt{n}$', r'$1/{n^{1/3}}$',
                                                                r'$1/\log^{2}(n)$', r'$1/\log(n)$']
else:
    p_actions = [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1]
    labels = ['${0}$'.format(i) for i in p_actions]

if seed is not None:
    np.random.seed(seed)
pi = np.random.permutation(n) if seed is not None else np.array([i for i in range(n)])

metricList = [Metric.SpinGlass, Metric.Magnetization]
rules = [[np.random.choice(a=[Rule.STABLE, Rule.UNSTABLE], p=[p, 1 - p]) for i in range(n)] for p in p_actions]

state = '$p_{stable}$'
c_len = 'length'
data = {c_len: [], state: []}
for metric in metricList:
    data[metric.name] = []
conf = createConfig(c_type, n=n)

states = np.random.choice(a=[State.ON, State.OFF], size=size, p=[p_state, 1 - p_state])
conf.set_states(states)
for i, p in enumerate(p_actions):
    conf.set_rules(rules[i])
    evol, metrics = evolve(config=conf, perm=pi, steps=steps, metricList=metricList, cycleBreak=True)
    data[c_len].append(cycle_length(evol)[0])
    data[state].append(labels[i])
    for e in metrics:
        data[e.name].append(metrics[e][-1])

datum = pd.DataFrame(data)

csv = datum.to_csv(encoding='utf-8', index=False)
print(csv)
