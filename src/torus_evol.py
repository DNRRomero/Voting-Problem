import numpy as np
import pandas as pd
import argparse

from modules.data_structure import ConfigType
from modules.utils import create_config, states_per_magnet, cycle_length, rules_per_factor
from modules.Evolve import evolve, setup
from modules.metric import Metric

dpn = 'Samples random Torus configuration, keeping track of energy and consensus'
parser = argparse.ArgumentParser(description=dpn)
parser.add_argument('n', type=int, help='Length of side of grid')
parser.add_argument('seed', type=int, help='Seed for choosing permutation')
parser.add_argument('steps', type=int, help='Number of steps to simulate')

args = parser.parse_args()

size = args.n ** 2
c_type = ConfigType.Torus
config = create_config(configType=c_type, n=args.n)
np.random.seed(args.seed)
pi = np.random.permutation(size)
stableList = [0.2 * i for i in range(6)] + [0.5]

rules, metrics = setup()
out = {'stability': [], 'step': [], 'length': [], 'cycle_start': [], 'Energy': [], 'Consensus': []}
metricList = [Metric.SpinGlass, Metric.Magnetization]

for stab in stableList:
    init_states = states_per_magnet(size, 0.0)
    init_rules = rules_per_factor(size, stab)
    config.set_states(init_states).set_rules(init_rules)
    evol, result = evolve(config=config, perm=pi, steps=args.steps, metricList=metricList, cycleBreak=True)
    length, start = cycle_length(evol)
    end = evol.shape[0] if length == args.steps + 2 else start + length
    for i in range(end):
        out['stability'].append(stab)
        out['cycle_start'].append(start)
        out['length'].append(length)
        out['step'].append(i)
        out['Energy'].append(result[Metric.SpinGlass][i])
        out['Consensus'].append(result[Metric.Magnetization][i])

df = pd.DataFrame(out)
csv = df.to_csv(encoding='utf-8', index=False)
print(csv)
