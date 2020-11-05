import numpy as np
import pandas as pd
from data_structure import State, Rule, ConfigType
from metric import Metric, magnetization
from utils import createConfig, cycle_length
from Evolve import evolve

n = 256
c_type = ConfigType.Ring
size = n
p_state = 0.5
seed = 654798203
steps = 2000
np.random.seed(seed)
pi = np.random.permutation(n)
metricList = [Metric.SpinGlass, Metric.Magnetization]
magnetList = [0]


agree = {'init_magnet': [], 'length': [], 'Magnetization_mean': [], 'Magnetization_min': [], 'Magnetization_max': [],
         'Magnetization_std': [], 'SpinGlass': [], 'unstables': []}
conf = createConfig(ConfigType.Ring, n=n)

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
        array, out = evolve(conf, perm=pi, steps=steps,
                            metricList=metricList, cycleBreak=True)
        curr_energy = out[Metric.SpinGlass][-1]
        curr_magnet = out[Metric.Magnetization][-1]
        length, start = cycle_length(array)

        stables = [k for k in range(n) if curr_rule[k] == Rule.STABLE]
        agree['init_magnet'].append(mag)
        agree['length'].append(length)
        agree['Magnetization_mean'].append(curr_magnet)
        agree['Magnetization_std'].append(np.std(magnetization(array[start: start + length])))
        agree['Magnetization_min'].append(np.min(magnetization(array[start: start + length])))
        agree['Magnetization_max'].append(np.max(magnetization(array[start: start + length])))
        agree['SpinGlass'].append(curr_energy)
        agree['unstables'].append(n - len(stables))

        # Choose a random stable node to change rule
        index = 0 if stables == [] else np.random.choice(stables)
        curr_rule[index] = Rule.UNSTABLE
        conf.set_rules(curr_rule)
data = pd.DataFrame(agree)
csv = data.to_csv(encoding='utf-8', index=False)
print(csv)
