import numpy as np
import pandas as pd
import argparse
from .modules.data_structure import ConfigType, Rule
from .modules.metric import Metric
from .modules.utils import create_config, states_per_magnet, cycle_length
from .modules.Evolve import evolve


def chess_config(n, width):
    assert width > 0
    c_type = ConfigType.Torus
    size = n ** 2
    # rule_set = lambda x, y: (x + y) % 2
    rule_set = lambda x,y: (((x//width)%2 ) + ((y//width) %2)) %2
    pair = lambda k: (k // n, k % n)
    assign = lambda i: Rule.STABLE if i == 0 else Rule.UNSTABLE
    rules = [assign(rule_set(pair(i)[0], pair(i)[1])) for i in range(size)]

    return create_config(c_type, n=n, m=n, rules=rules)


def blot_config(n, thick):
    c_type = ConfigType.Torus
    size = n ** 2
    pair = lambda k: (k // n, k % n)
    rule_set = lambda x, y: 1 if x <= thick and y <= thick else -1
    assign = lambda i: Rule.STABLE if i == 1 else Rule.UNSTABLE
    rules = [assign(rule_set(pair(i)[0], pair(i)[1])) for i in range(size)]

    return create_config(c_type, n=n, m=n, rules=rules)


def wall_config(n, thick):
    c_type = ConfigType.Torus
    size = n ** 2
    pair = lambda k: (k // n, k % n)
    rule_set = lambda x, y: 1 if x <= thick else -1
    assign = lambda i: Rule.STABLE if i == 1 else Rule.UNSTABLE
    rules = [assign(rule_set(pair(i)[0], pair(i)[1])) for i in range(size)]

    return create_config(c_type, n=n, m=n, rules=rules)


def strands_config(n, n_strands):
    c_type = ConfigType.Torus
    size = n ** 2
    rng = np.random.default_rng()
    strands = rng.choice(n, size=n_strands, replace=False)
    pair = lambda k: (k // n, k % n)
    rule_set = lambda x, y: 1 if x in strands else -1
    assign = lambda i: Rule.STABLE if i == 1 else Rule.UNSTABLE
    rules = [assign(rule_set(pair(i)[0], pair(i)[1])) for i in range(size)]

    return create_config(c_type, n=n, m=n, rules=rules)


def checked_config(n, check_size):
    c_type = ConfigType.Torus
    size = n ** 2
    rule_set = lambda x, y: -1 if (x % (check_size+1) == 0 or y % (check_size+1) == 0) else 1
    pair = lambda k: (k // n, k % n)
    assign = lambda i: Rule.STABLE if i == 1 else Rule.UNSTABLE
    rules = [assign(rule_set(pair(i)[0], pair(i)[1])) for i in range(size)]

    return create_config(c_type, n=n, m=n, rules=rules)


def unstable_shape_sample(args):
    config_set = {'chess': chess_config, 'blot': blot_config,
                  'wall': wall_config, 'strand': strands_config, 'check': checked_config}
    config = config_set[args.scheme](args.n, args.param)
    size = args.n**2
    np.random.seed(args.seed)
    pi = np.random.permutation(size)
    magnetList = [2*i/10 for i in range(6)] +[0.5]
    metricList = [Metric.SpinGlass, Metric.Magnetization]
    out = {'length': [], 'init_magnet': [], 'Energy': [], 'Consensus': []}
    for mag in magnetList:
        states = states_per_magnet(size, mag)
        config.set_states(states)
        evol, metrics = evolve(config=config, perm=pi, steps=args.steps, metricList=metricList, cycleBreak=True)
        length, _ = cycle_length(evol)
        out['length'].append(length)
        out['init_magnet'].append(mag)
        out['Energy'].append(metrics[Metric.SpinGlass][-1])
        out['Consensus'].append(metrics[Metric.Magnetization][-1])
    df = pd.DataFrame(out)
    csv = df.to_csv(encoding='utf-8', index=False)
    print(csv)


if __name__ == "__main__":
    dpn = 'Samples random Torus configuration, where instability scheme is obtained from one of possible settings'
    parser = argparse.ArgumentParser(description=dpn)
    parser.add_argument('n', type=int, help='Length of side of Torus')
    scheme_dpn = "Type of assignment of unstable nodes (i.e. 'chess', 'wall', 'strand', 'blot' or 'check') "
    parser.add_argument('scheme', help=scheme_dpn)
    param_dpn = "Accompanying parameter for chosen scheme: \n Chess: ignored \n wall: thickness " \
                "\n strand: number of strands \n blot: blot width \n check: check size"
    parser.add_argument('param', help=param_dpn)
    parser.add_argument('seed', type=int, help='Seed for choosing permutation')
    parser.add_argument('steps', type=int, help='Number of steps to simulate')

    args = parser.parse_args()

    unstable_shape_sample(args)
