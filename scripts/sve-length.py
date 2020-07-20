#!/usr/bin/env python3

import os
import sys
from pathlib import Path

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import seaborn as sea
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def read_data(application: str):
  data = pd.DataFrame()
  for w in [128,256,512,1024,2048]:
    next_data = pd.read_csv(f'../data/{application}/stats-{w}.csv')
    next_data['svewidth'] = w
    data = data.append(next_data, ignore_index=True)

  return data


def plot_both_cpus(application: str, data, out_dir, level: int):
  g = sea.catplot(x='svewidth', y='miss-ratio', hue='config', kind='bar',
                  data=data[data.level == level],
                  palette='colorblind', ci=False, legend_out=False)

  plt.xlabel('sve width (bits)')
  plt.ylabel('miss ratio (%)')
  plt.legend(loc='upper left')

  g.savefig(out_dir / f'{application}-svewidth-both-L{level}.pdf', bbox_inches='tight')


if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("Usage: sve-length.py <application>")
    sys.exit(1)

  script_dir = Path(os.path.dirname(os.path.realpath(__file__)))
  out_dir = script_dir / '../figures/svewidth'
  os.makedirs(out_dir, exist_ok=True)

  application = sys.argv[1]
  data = read_data(application)
  data['miss-ratio'] = data.misses / data.accesses * 100

  sea.set(style='whitegrid')

  plot_both_cpus(application, data, out_dir, 1)
  plot_both_cpus(application, data, out_dir, 2)
