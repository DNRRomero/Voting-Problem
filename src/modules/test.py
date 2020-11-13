from . import Evolve
from . import Plotter
from . import Ring
from . import Torus
from .metric import *
from . import utils


def torus():
    n = 20
    m = 20
    g = lambda x: 1 / np.sqrt(x)
    p_action = 0.5
    p_state = 0.5
    steps = 50
    pi = np.random.permutation(n * m)

    toro = Torus.createTorus(n, m, p_action, p_state)
    evol, metrics = Evolve.evolve(toro, pi, steps, sequential=False)
    title = str(n) + 'x' + str(m) + 'Torus'
    fig = Plotter.animate(evol, title=title, shape=(n, m), save=False, interval=200)


def ring():
    n = 100
    p_action = 0.5
    p_state = 0.5
    steps = 50
    pi = np.random.permutation(n)
    anillo = Ring.createRing(n, p_action, p_state)
    evol, metrics = Evolve.evolve(anillo, pi, steps, sequential=False)
    title = str(n) + ' Ring'
    fig = Plotter.animate(evol, title=title, shape=(1, n), save=False, interval=800)


def blocks():
    k = 6
    primes = utils.primes_up_to(k)
    n = primes.sum() + 3 * len(primes)
    pi = np.array([i for i in range(n)])
    states = [0 for i in range(n)]
    j = 2
    for p in primes:
        for t in range(p + 1):
            states[j + t] = State.OFF
        states[(j + p + 1) % n] = State.ON
        states[(j + p + 2) % n] = State.ON
        j = j + p + 3

    j = 2
    rules = [0 for i in range(n)]
    for p in primes:
        for t in range(p - 1):
            rules[j + t] = Rule.UNSTABLE
        for i in range(4):
            rules[(j + p - 1 + i) % n] = Rule.STABLE
        j = j + p + 3

    ring = Ring.createRing(n, 0.5, 0.5)
    ring.set_states(states)
    ring.set_rules(rules)

    evol, metrics = Evolve.evolve(ring, pi, 90, metricList=[Metric.Density, Metric.Energy], sequential=False)

    Plotter.plot_metrics(metrics)


if __name__ == "__main__":
    test = 0
    torus() if test else blocks()
