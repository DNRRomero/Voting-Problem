import networkx as nx
import numpy as np


def create(size: int, g_type: str, seed=None, **kwargs):
    n = int(np.sqrt(size))
    m = size // n
    factory = {
        'hex': nx.generators.hexagonal_lattice_graph(n=n, m=m, periodic=True),
        'internet': nx.generators.random_internet_as_graph(n=size, seed=seed),
        'regular': nx.generators.random_regular_graph(n=size, seed=seed, **kwargs),
        'small-world': nx.generators.connected_watts_strogatz_graph(n=n, seed=seed, **kwargs),
    }
    G = factory.get(g_type)
    return nx.adjacency_matrix(G)
