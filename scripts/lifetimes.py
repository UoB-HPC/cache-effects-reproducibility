#!/usr/bin/env python3

import math
import os
import sys
from pathlib import Path

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import numpy as np
import seaborn as sea
import matplotlib.pyplot as plt
import matplotlib as mpl


def read_data(application: str):
  data = pd.DataFrame()
  for w in [128,256,512,1024,2048]:
    next_data = pd.read_csv(f'../data/{application}/lifetimes-{w}.csv')
    next_data['svewidth'] = w
    data = data.append(next_data, ignore_index=True)
  data = data[data.level <= 2]

  return data


# https://stackoverflow.com/questions/2413522/weighted-standard-deviation-in-numpy
def weighted_stddev(group):
    values, weights = group.time, group['count']
    average = np.average(values, weights=weights)
    variance = np.average((values-average)**2, weights=weights)
    return math.sqrt(variance)


def plot_one_cpu(application: str, data, out_dir, level='both'):
  if level != 'both':
    data = data[data.level == level]

  for config in ['TX2', 'A64FX']:
    g = sea.FacetGrid(data[(data.config == config)], row='level', col='svewidth', margin_titles=True).\
        map(sea.distplot, 'time', hist=True)

    g.set_axis_labels('lifetime in cache','ratio of entries')
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    levelname = 'both' if level == 'both' else f'L{level}'
    fname = f'{application}-lifetimes-{config}-{levelname}.pdf'
    g.savefig(out_dir / fname, bbox_inches='tight')
    print(f"Saved {fname}")

def plot_one_level_both_cpus(application: str, data, out_dir, level: int):
    g = sea.FacetGrid(data[(data.level == level)], row='config', col='svewidth', margin_titles=True, row_order=['TX2','A64FX']).\
      map(sea.distplot, 'time', hist=True)
    g.set_axis_labels('lifetime in cache','fraction of entries')
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    averages = data[data.level == 1].groupby(['svewidth','config']).apply(
      lambda g: np.ceil(np.average(g.time, weights=g['count']))).unstack()
    stddevs = data[data.level == 1 ].groupby(['svewidth','config']).apply(weighted_stddev).unstack()

    for row in zip([0,1], ['TX2','A64FX']):
      rowid, rowname = row
      for colid in range(5):
        colname = 128 * (2**colid)
        ax = g.axes[rowid, colid]
        text = f"μ = {averages.loc[colname, rowname]:.0f}\nσ = {stddevs.loc[colname, rowname]:.0f}"
        ax.text(0.6, 0.7, text, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)

    fname = f'{application}-lifetimes-both-L{level}.pdf'
    g.savefig(out_dir / fname, bbox_inches='tight')
    print(f"Saved {fname}")


if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("Usage: lifetimes.py <application>")
    sys.exit(1)

  script_dir = Path(os.path.dirname(os.path.realpath(__file__)))
  out_dir = script_dir / '../figures/lifetime'
  os.makedirs(out_dir, exist_ok=True)

  application = sys.argv[1]
  data = read_data(application)

  plot_one_cpu(application, data, out_dir, 'both')
  plot_one_cpu(application, data, out_dir, 1)
  plot_one_cpu(application, data, out_dir, 2)

  plot_one_level_both_cpus(application, data, out_dir, 1)
  plot_one_level_both_cpus(application, data, out_dir, 2)
