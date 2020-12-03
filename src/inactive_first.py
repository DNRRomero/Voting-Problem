import numpy as np
import pandas as pd
import argparse
import itertools
from numpy.random import default_rng

from modules.data_structure import ConfigType, State
from modules.utils import create_config, states_per_magnet, cycle_length, rules_per_factor
from modules.Evolve import setup, evolve, order_update
from modules.metric import Metric

dpn = 'Samples random Torus configuration, comparing consensus attained ' \
      'between a random permutation and one where inactive nodes are queried first'
parser = argparse.ArgumentParser(description=dpn)
parser.add_argument('n', type=int, help='Length of side of grid')
parser.add_argument('steps', type=int, help='Number of steps to simulate')
parser.add_argument("-f", '--first', type=int, default=0, help='first majority preference')
parser.add_argument("-s", '--second', type=int, default=1, help='second majority preference')

args = parser.parse_args()

assert (args.first != args.second)

size = args.n ** 2
c_type = ConfigType.Torus
config = create_config(configType=c_type, n=args.n)
magnetList = [-0.4, -0.3, -0.2, -0.1]
stabList = [0.0, 0.2, 0.4, 0.5, 0.6, 0.8]

pi = np.random.permutation(size)

rules, metrics = setup()
le = 'length'
out = {'init_magnet': [], 'Energy': [], 'Density': [], 'order': [], 'init_stab': [], le: []}

metricList = [Metric.Energy, Metric.Density]
rng = default_rng()
for mag, stab in itertools.product(magnetList, stabList):
    init_states = states_per_magnet(size, mag, State.OFF)
    init_rules = rules_per_factor(size, stab, pref1=args.first, pref2=args.second)
    config.set_states(init_states).set_rules(init_rules)
    array = np.zeros((args.steps + 1, config.size), dtype=np.int8)
    for index in range(config.size):
        array[0][index] = config.nodes[index].state
    t = 1
    cycle, length = None, None
    magn, last = 0, 0

    while t <= args.steps and magn != 1:
        inactive = np.array([i for i in range(config.size) if array[t-1][i] == State.OFF])
        active = np.array([i for i in range(config.size) if array[t-1][i] == State.ON])
        rng.shuffle(inactive)
        rng.shuffle(active)
        both = np.concatenate((inactive, active))
        array[t] = order_update(array[t - 1].copy(), config, both, rules)
        magn = metrics[Metric.Consensus](array[t], config, single=1)
        t += 1
    last = -1 if t > args.steps else t - 1

    for metric in metricList:
        out[metric.name].append(metrics[metric](array[last], config, single=1))
    out[le].append(0)
    out['order'].append('off_first')
    out['init_magnet'].append(mag)
    out['init_stab'].append(stab)

    # Now random order
    evol, vals = evolve(config=config, steps=args.steps, perm=pi, metricList=metricList, cycleBreak=True)
    length, start = cycle_length(evol)
    out[le].append(length)
    for metric in metricList:
        out[metric.name].append(vals[metric][-1])
    out['order'].append('random')
    out['init_magnet'].append(mag)
    out['init_stab'].append(stab)

df = pd.DataFrame(out)
csv = df.to_csv(encoding='utf-8', index=False)
print(csv)
