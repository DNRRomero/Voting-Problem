import numpy as np
import pandas as pd
import argparse

from modules.data_structure import ConfigType, State
from modules.utils import create_config, states_per_magnet, cycle_length
from modules.Evolve import cycleCheck, setup, evolve
from modules.metric import Metric

dpn = 'Samples random Torus configuration, comparing consensus attained ' \
      'between a random permutation and one where inactive nodes are queried first'
parser = argparse.ArgumentParser(description=dpn)
parser.add_argument('n', type=int, help='Length of side of grid')
parser.add_argument('steps', type=int, help='Number of steps to simulate')

args = parser.parse_args()

size = args.n ** 2
c_type = ConfigType.Torus
config = create_config(configType=c_type, n=args.n)
magnetList = [0.0]
pi = np.random.permutation(size)

rules, metrics = setup()
out = {'init_magnet': [], 'Energy': [], 'Consensus': [], 'order': [], 'length': []}
metricList = [Metric.SpinGlass, Metric.Magnetization]

for mag in magnetList:
    init_states = states_per_magnet(size, mag, State.OFF)
    config.set_states(init_states)
    array = np.zeros((args.steps + 1, config.size), dtype=np.int8)
    for index in range(config.size):
        array[0][index] = config.nodes[index].state
    t = 1
    cycle, length = None, None

    while t <= args.steps and cycle is None:
        array[t] = array[t - 1]
        inactive = np.array([i for i in range(config.size) if array[t][i] == State.OFF])
        active = np.array([i for i in range(config.size) if array[t][i] == State.ON])
        np.random.seed()
        np.random.shuffle(inactive)
        np.random.shuffle(active)
        both = np.concatenate((inactive, active))
        for index in both:
            state = rules[config.nodes[index].rule](t, array, config, index)
            array[t][index] = state
        cycle, length = cycleCheck(config, args.steps, array, t)

    if cycle is not None:
        # If there is a cycle, copy the average metric value in cycle at the last entry
        out['Energy'].append(metrics[Metric.SpinGlass](array[cycle], single=1))
        out['Consensus'].append(np.mean(metrics[Metric.Magnetization](array[cycle: cycle + length])))
        out['length'].append(length)
    else:
        out['Energy'].append(metrics[Metric.SpinGlass](array[-1], single=1))
        out['Consensus'].append(metrics[Metric.Magnetization](array[-1], single=1))
        out['length'].append(args.steps + 2)
    out['order'].append('off_first')
    out['init_magnet'].append(mag)

    # Now random order
    evol, vals = evolve(config=config, steps=args.steps, perm=pi, metricList=metricList, cycleBreak=True)
    length, start = cycle_length(evol)
    out['length'].append(length)
    out['Energy'].append(vals[Metric.SpinGlass][-1])
    out['Consensus'].append(vals[Metric.Magnetization][-1])
    out['order'].append('random')
    out['init_magnet'].append(mag)

df = pd.DataFrame(out)
csv = df.to_csv(encoding='utf-8', index=False)
print(csv)
