import Evolve
import Torus, Ring
from metric import *


def torus():
    n = 20
    m = 20
    g = lambda x: 1 / np.sqrt(x)
    p_action = 0.5
    p_state = 0.5
    steps = 50
    pi = np.random.permutation(n * m)

    torus = Torus.createTorus(n, m, p_action, p_state)
    evol = Evolve.evolve(torus, pi, steps, sequential=False)[Metric.EV]
    title = str(n) + 'x' + str(m) + 'Torus'
    fig = Evolve.animate(evol, title=title, shape=(n, m), save=False, interval=200)
    # fig = Evolve.plot_grid(evol, title='torus', shape=(10,10))


def ring():
    n = 100
    p_action = 0.5
    p_state = 0.5
    steps = 50
    pi = np.random.permutation(n)
    ring = Ring.createRing(n, p_action, p_state)
    evol = Evolve.evolve(ring, pi, steps, sequential=False)[Metric.EV]
    title = str(n) + ' Ring'
    fig = Evolve.animate(evol, title=title, shape=(1, n), save=False, interval=800)


if __name__ == "__main__":
    test = 1
    torus() if test else ring()