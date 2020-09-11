from rules import *
from metric import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def evolve(config: Config, perm: np.ndarray, steps=100, metricList=None, sequential: bool = True):
    """
    :param sequential:
    :param config:
    :param perm:
    :param steps:
    :param metricList:
    :return:
    """
    if metricList is None:
        metricList = []
    rules = getRules()
    metrics = getMetrics()
    out = {}
    seq = config.size if sequential else 1
    array = np.zeros((steps*seq + 1, config.size))
    for index in range(config.size):
        array[0][index] = config.nodes[index].state
    t = 1
    if sequential:
        while t <= config.size * steps:
            for index in perm:
                array[t] = array[t - 1]
                state = rules[config.nodes[index].rule](t - 1, array, config, index)
                array[t][index] = state
                t += 1

    else:
        while t <= steps:
            for index in perm:
                state = rules[config.nodes[index].rule](t - 1, array, config, index)
                array[t][index] = state
            t += 1

    for metric in metricList:
        out[Metric.metric] = metrics[metric](array, config)

    out[Metric.EV] = array
    return out


def plot_grid(evolution, shape=None, sl=-1, title='', colormap='Greys', vmin=None, vmax=None,
              node_annotations=None, show_grid=False):
    if shape is not None:
        evolution = evolution.reshape((len(evolution), shape[0], shape[1]))[sl]
    cmap = plt.get_cmap(colormap)
    plt.title(title)
    plt.imshow(evolution, interpolation='none', cmap=cmap, vmin=vmin, vmax=vmax)

    if node_annotations is not None:
        for i in range(len(node_annotations)):
            for j in range(len(node_annotations[i])):
                plt.text(j, i, node_annotations[i][j], ha="center", va="center", color="grey",
                         fontdict={'weight': 'bold', 'size': 6})

    if show_grid:
        plt.grid(which='major', axis='both', linestyle='-', color='grey', linewidth=0.5)
        plt.xticks(np.arange(-.5, len(evolution[0]), 1), "")
        plt.yticks(np.arange(-.5, len(evolution), 1), "")
        plt.tick_params(axis='both', which='both', length=0)

    plt.show()


def animate(activities, title='', shape=None, save=False, interval=500, colormap='Greys', vmin=None, vmax=None,
            name='evolved'):
    if shape is not None:
        activities = _reshape_for_animation(activities, shape)
    cmap = plt.get_cmap(colormap)
    fig, ax = plt.subplots()
    ax.set_title(title)
    im = ax.imshow(activities[0], cmap=cmap, vmin=vmin, vmax=vmax)

    def update_fig(index):

        im.set_array(activities[index])
        ax.set_xlabel('Step '+str(index))
        return im,

    ani = animation.FuncAnimation(fig, update_fig, frames=len(activities), interval=interval, blit=True)
    if save:
        ani.save(name + '.gif', dpi=80, writer="imagemagick")
    return ani


def _reshape_for_animation(evol, shape):
    if len(shape) == 1:
        assert shape[0] == len(evol[0]), "shape must equal the length of an activity vector"
        new_activities = []
        for i, a in enumerate(evol):
            new_activity = []
            new_activity.extend(evol[0:i + 1])
            while len(new_activity) < len(evol):
                new_activity.append([0] * len(evol[0]))
            new_activities.append(new_activity)
        return np.array(new_activities)
    elif len(shape) == 2:
        return np.reshape(evol, (len(evol), shape[0], shape[1]))
    else:
        raise Exception("shape must be a tuple of length 1 or 2")


def plot_metrics(metrics):
    fig, axs = plt.subplots(nrows=len(metrics), sharex='all')
    for i, metric in enumerate(metrics):
        data = metrics[str(metric)]
        axs[i].set_title(metric)
        axs[i].plot(range(len(data)), data)

