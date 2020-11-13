import numpy as np
import pandas as pd
import argparse

from modules.Evolve import evolve
from modules.data_structure import ConfigType, Rule, State
from modules.metric import Metric
from modules.utils import create_config, cycle_length

dpn = 'Samples random Ring configuration, keeping track of limit cycle information'
parser = argparse.ArgumentParser(description=dpn)
parser.add_argument('n', type=int, help='Length of ring')
parser.add_argument('stab_range', help='Type of assignment of stable nodes (i.e. "var" or "fixed" ')
parser.add_argument('seed', type=int, help='Seed for choosing permutation. If seed=-1, canon permutation')
parser.add_argument('steps', type=int, help='Number of steps to simulate')

args = parser.parse_args()

size = args.n
c_type = ConfigType.Ring
p_state = 0.5

p_actions = None
labels = None
if args.stab_range == 'var':
    p_actions = [0, 1 / np.power(size, 2), 1 / np.power(size, 1.5), 1 / size, 1 / np.sqrt(size),
                 1 / np.power(size, 1 / 3),
                 1 / np.power(np.log2(size), 2), 1 / np.log2(size)]
    labels = [r'$0$', r'$1/n^2$', r'$1/n^{3/2}$', r'$1/n$', r'$1/\sqrt{n}$', r'$1/{n^{1/3}}$',
              r'$1/\log^{2}(n)$', r'$1/\log(n)$']
else:
    p_actions = [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1]
    labels = ['${0}$'.format(i) for i in p_actions]

if args.seed != -1:
    np.random.seed(args.seed)
pi = np.random.permutation(args.n) if args.seed != -1 else np.array([i for i in range(args.n)])

metricList = [Metric.Energy, Metric.Consensus]
np.random.seed()
rules = [[np.random.choice(a=[Rule.STABLE, Rule.UNSTABLE], p=[p, 1 - p]) for i in range(args.n)] for p in p_actions]

state = '$p_{stable}$'
c_len = 'length'
data = {c_len: [], state: []}
for metric in metricList:
    data[metric.name] = []
conf = create_config(c_type, n=args.n)

states = np.random.choice(a=[State.ON, State.OFF], size=size, p=[p_state, 1 - p_state])
conf.set_states(states)
for i, p in enumerate(p_actions):
    conf.set_rules(rules[i])
    evol, metrics = evolve(config=conf, perm=pi, steps=args.steps, metricList=metricList, cycleBreak=True)
    data[c_len].append(cycle_length(evol)[0])
    data[state].append(labels[i])
    for e in metrics:
        data[e.name].append(metrics[e][-1])

datum = pd.DataFrame(data)

csv = datum.to_csv(encoding='utf-8', index=False)
print(csv)
