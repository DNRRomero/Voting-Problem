import numpy as np
import pandas as pd
import argparse

from modules.data_structure import State, Rule, ConfigType
from modules.metric import Metric, magnetization
from modules.utils import create_config, cycle_length
from modules.Evolve import evolve

dpn = 'Samples random Ring configuration, keeping track of consensus and energy when randomly adding unstability'
parser = argparse.ArgumentParser(description=dpn)
parser.add_argument('n', type=int, help='Length of Ring')
parser.add_argument('seed', type=int, help='Seed for choosing permutation. If seed=-1, canon permutation')
parser.add_argument('steps', type=int, help='Number of steps to simulate')

args = parser.parse_args()

if args.seed == -1:
    args.seed = None

c_type = ConfigType.Ring
size = args.n
p_state = 0.5

np.random.seed(args.seed)
pi = np.random.permutation(args.n)
metricList = [Metric.SpinGlass, Metric.Magnetization]
magnetList = [0, 0.2, 0.4, 0.6, 0.8]

agree = {'init_magnet': [], 'length': [], 'Magnetization_mean': [], 'Magnetization_min': [], 'Magnetization_max': [],
         'Magnetization_std': [], 'SpinGlass': [], 'unstables': []}
conf = create_config(ConfigType.Ring, n=args.n)

for i, mag in enumerate(magnetList):
    init_states = [State.ON] * round((size * (0.5 + mag / 2)) - 10 ** (-9)) + [State.OFF] * round(
        (size * (0.5 - mag / 2) + 10 ** (-9)))
    np.random.seed()
    np.random.shuffle(init_states)
    init_rule = np.array([Rule.STABLE] * size)
    curr_rule = init_rule
    conf.set_rules(init_rule)
    conf.set_states(init_states)
    curr_magnet = mag
    stables = [0]
    while curr_magnet < 1 and stables != []:
        array, out = evolve(conf, perm=pi, steps=args.steps,
                            metricList=metricList, cycleBreak=True)
        curr_energy = out[Metric.SpinGlass][-1]
        curr_magnet = out[Metric.Magnetization][-1]
        length, start = cycle_length(array)

        stables = [k for k in range(args.n) if curr_rule[k] == Rule.STABLE]
        agree['init_magnet'].append(mag)
        agree['length'].append(length)
        agree['Magnetization_mean'].append(curr_magnet)
        agree['Magnetization_std'].append(np.std(magnetization(array[start: start + length])))
        agree['Magnetization_min'].append(np.min(magnetization(array[start: start + length])))
        agree['Magnetization_max'].append(np.max(magnetization(array[start: start + length])))
        agree['SpinGlass'].append(curr_energy)
        agree['unstables'].append(args.n - len(stables))

        # Choose a random stable node to change rule
        index = 0 if stables == [] else np.random.choice(stables)
        curr_rule[index] = Rule.UNSTABLE
        conf.set_rules(curr_rule)
data = pd.DataFrame(agree)
csv = data.to_csv(encoding='utf-8', index=False)
print(csv)
