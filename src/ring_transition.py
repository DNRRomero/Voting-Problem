import numpy as np
import pandas as pd
from numpy.random import default_rng
import argparse

from modules.Evolve import evolve
from modules.data_structure import ConfigType, Rule, State
from modules.metric import Metric
from modules.utils import create_config, cycle_length, rules_per_ratio, states_per_magnet

dpn = 'Samples random Torus configuration, keeping track of limit cycle information'
parser = argparse.ArgumentParser(description=dpn)
parser.add_argument('n', type=int, help='Length of side of grid')
parser.add_argument('seed', type=int, help='Seed for choosing permutation. If seed=-1, canon permutation')
parser.add_argument('steps', type=int, help='Number of steps to simulate')

args = parser.parse_args()

c_type = ConfigType.Ring
p_state = 0.5

r_factor = [4 * i for i in range(21)]

if args.seed != -1:
    np.random.seed(args.seed)
pi = np.random.permutation(args.n) if args.seed is not None else np.array([i for i in range(args.n)])

rng = default_rng()

metricList = [Metric.Energy, Metric.Consensus]

state = '$r_{stable}$'
c_len = 'length'
data = {c_len: [], state: [], 'fct': []}
for metric in metricList:
    data[metric.name] = []
conf = create_config(c_type, n=args.n)

states = states_per_magnet(args.n, 0.0)
conf.set_states(states)
for i, p in enumerate(r_factor):
    rules = rules_per_ratio(args.n, p)
    conf.set_rules(rules)
    evol, metrics = evolve(config=conf, perm=pi, steps=args.steps, metricList=metricList, cycleBreak=True)
    data[c_len].append(cycle_length(evol)[0])
    data[state].append(p/args.n)
    data['fct'].append(p)
    for e in metrics:
        data[e.name].append(metrics[e][-1])

datum = pd.DataFrame(data)

csv = datum.to_csv(encoding='utf-8', index=False)
print(csv)
