import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

n = 150
g = lambda x: 1 / np.sqrt(x)
p_stab = g(n)
p_state = 0.5

pi = np.random.permutation(n)



