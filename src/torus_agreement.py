import numpy as np
import pandas as pd

from modules.data_structure import State, Rule, ConfigType
from modules.metric import Metric, magnetization
from modules.utils import createConfig, cycle_length
from modules.Evolve import evolve

n = 20
c_type = ConfigType.Torus
size = n**2
p_state = 0.5
seed = 654798203
steps = 3500
np.random.seed(seed)
pi = np.random.permutation(size)
metricList = [Metric.SpinGlass, Metric.Magnetization]
magnetList = [0, 0.2, 0.4, 0.6, 0.8]

agree = {'init_magnet': [], 'length': [], 'Magnetization_mean': [], 'Magnetization_min': [], 'Magnetization_max': [],
         'Magnetization_std': [], 'SpinGlass': [], 'unstables': []}
conf = createConfig(ConfigType.Torus, n=n)

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

        stables = [k for k in range(size) if curr_rule[k] == Rule.STABLE]
        agree['init_magnet'].append(mag)
        agree['length'].append(length)
        agree['Magnetization_mean'].append(curr_magnet)
        agree['Magnetization_std'].append(np.std(magnetization(array[start: start + length])))
        agree['Magnetization_min'].append(np.min(magnetization(array[start: start + length])))
        agree['Magnetization_max'].append(np.max(magnetization(array[start: start + length])))
        agree['SpinGlass'].append(curr_energy)
        agree['unstables'].append(size - len(stables))

        # Choose a random stable node to change rule
        index = 0 if stables == [] else np.random.choice(stables)
        curr_rule[index] = Rule.UNSTABLE
        conf.set_rules(curr_rule)
data = pd.DataFrame(agree)
csv = data.to_csv(encoding='utf-8', index=False)
print(csv)
