import numpy as np
from matplotlib import pyplot as plt, animation as animation
from .data_structure import Config, ConfigType
import seaborn as sns


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


def plot_config(config: Config, which='both'):
    rules = np.array(config.get_rules())
    states = np.array(config.get_states())

    if config.type == ConfigType.Torus:
        side = int(np.sqrt(config.size))
        rules = rules.reshape((side, side))
        states = states.reshape((side, side))
    option = rules if which == 'rule' else states

    cmap = plt.get_cmap('Greys')
    if which == 'both':
        fig, axs = plt.subplots(1,2)
        ax_r, ax_s = axs
        ax_r.set_title('Node rule visualization')
        ax_s.set_title('Node state visualization')
        im = ax_r.imshow(rules, cmap=cmap)
        im = ax_s.imshow(states, cmap=cmap)
        ax_r.set_yticks([])
        ax_s.set_yticks([])
        ax_r.set_xticks([])
        ax_s.set_xticks([])

    elif which == 'rule' or which == 'state':
        fig, ax = plt.subplots()
        title = ''
        ax.set_title(title)
        im = ax.imshow(option, cmap=cmap)
        ax.set_yticks([])
        ax.set_xticks([])

    else:
        assert False
    return fig


def plot_config_sns(config: Config, which='both'):
    rules = np.array(config.get_rules())
    states = np.array(config.get_states())

    if config.type == ConfigType.Torus:
        side = int(np.sqrt(config.size))
        rules = rules.reshape((side, side))
        states = states.reshape((side, side))
    option = rules if which == 'rule' else states

    cmap = plt.get_cmap('Greys')
    if which == 'both':
        fig, axs = plt.subplots(1,2)
        ax_r, ax_s = axs
        ax_r.set_title('Node rule visualization')
        ax_s.set_title('Node state visualization')
        sns.heatmap(rules, ax=ax_r, xticklabels=False, yticklabels=False, cbar=False, square=True)
        sns.heatmap(states, ax=ax_s, xticklabels=False, yticklabels=False, cbar=False, square=True)

    elif which == 'rule' or which == 'state':
        fig, ax = plt.subplots()
        title = 'Node {0} visualization'.format(which)
        ax.set_title(title)
        im = ax.imshow(option, cmap=cmap)
        ax.set_yticks([])
        ax.set_xticks([])

    else:
        assert False


def animate(activities, title='', shape=None, save=False, interval=500, colormap='Greys', vmin=None, vmax=None,
            name='evolved'):
    if shape is not None:
        activities = _reshape_for_animation(activities, shape)
    cmap = plt.get_cmap(colormap)
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_yticks([])
    im = ax.imshow(activities[0], cmap=cmap, vmin=vmin, vmax=vmax)

    def update_fig(index):

        im.set_array(activities[index])
        ax.set_xlabel('Step ' + str(index))
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


def plot_metrics(metrics, shape=None):
    fig, ax = plt.subplots(nrows=len(metrics), sharex='all')
    if type(ax) != np.ndarray:
        for metric in metrics:
            data = metrics[metric]
            ax.plot(range(len(data)), data)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.set_title(metric.name)
    else:
        for i, metric in enumerate(metrics):
            data = metrics[metric]
            ax[i].plot(range(len(data)), data)
            ax[i].spines['top'].set_visible(False)
            ax[i].spines['right'].set_visible(False)
            ax[i].set_title(metric.name)


def plot_multi_metrics(metrics, labels, title=''):
    fig, ax = plt.subplots(nrows=len(metrics), sharex='all')
    if type(ax) != np.ndarray:
        for metric in metrics:
            plots = [j for j in range(len(metrics[metric]))]
            Data = metrics[metric]
            for j, data in enumerate(Data):
                plot, = ax.plot(range(len(data)), data, label=labels[j])
                plots[j] = plot
                ax.set_title(metric.name)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.legend(handles=plots, title=title, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.show()

    else:
        for i, metric in enumerate(metrics):
            plots = [j for j in range(len(metrics[metric]))]
            Data = metrics[metric]
            ax[i].spines['top'].set_visible(False)
            ax[i].spines['right'].set_visible(False)
            ax[i].set_title(metric.name)
            for j, data in enumerate(Data):
                plot, = ax[i].plot(range(len(data)), data, label=labels[j])
                plots[j] = plot
            ax[i].spines['top'].set_visible(False)
            ax[i].spines['right'].set_visible(False)
            ax[i].set_title(metric.name)
            ax[i].legend(handles=plots, title=title, loc='upper right')
        plt.show()


def plot_cycle_hist(dataFrame, var, disc=True, plot=sns.histplot, stat="probability", **kwargs):
    facet = sns.FacetGrid(dataFrame,  # the dataframe to pull from
                          row="$p_{stable}$",  # define the column for each subplot row to be differentiated by
                          hue="$p_{stable}$",  # define the column for each subplot color to be differentiated by
                          aspect=10,  # aspect * height = width
                          height=1.5,  # height of each subplot
                          )
    facet.map(plot, var, discrete=disc, stat=stat, **kwargs)

    def label(x, color, label):
        ax = plt.gca()  # get the axes of the current object
        ax.text(0, .2,  # location of text
                label,  # text label
                fontweight="bold", color=color, size=18,  # text attributes
                ha="left", va="center",  # alignment specifications
                transform=ax.transAxes)  # specify axes of transformation

    facet.map(label, var)  # the function counts as a plotting object!

    facet.set_titles("")  # set title to blank
    facet.set(yticks=[])  # set y ticks to blank
    facet.despine(bottom=True, left=True)  # remove 'spines'

    return facet


def plot_energy_kde(dataFrame, var):
    facet = sns.FacetGrid(dataFrame,  # the dataframe to pull from
                          row="p_a",  # define the column for each subplot row to be differentiated by
                          hue="p_a",  # define the column for each subplot color to be differentiated by
                          aspect=10,  # aspect * height = width
                          height=1.5,  # height of each subplot
                          )
    facet.map(sns.kdeplot, var, shade=True, alpha=1, lw=1.5, bw_adjust=0.2)
    facet.map(sns.kdeplot, var, lw=4, bw_adjust=0.2)
    facet.map(plt.axhline, y=0, lw=4)

    def label(x, color, label):
        ax = plt.gca()  # get the axes of the current object
        ax.text(0, .2,  # location of text
                label,  # text label
                fontweight="bold", color=color, size=20,  # text attributes
                ha="left", va="center",  # alignment specifications
                transform=ax.transAxes)  # specify axes of transformation

    facet.map(label, var)  # the function counts as a plotting object!

    facet.set_titles("")  # set title to blank
    facet.set(yticks=[])  # set y ticks to blank
    facet.despine(bottom=True, left=True)  # remove 'spines'

    return facet
