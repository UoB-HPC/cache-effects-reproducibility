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
  data = pd.read_csv(f'../data/{application}/scaling-512.csv')
  return data


def draw_heatmap(*args, **kwargs):
    # https://stackoverflow.com/questions/41471238/how-to-make-heatmap-square-in-seaborn-facetgrid
    data = kwargs.pop('data')
    d = data.pivot(index=args[1], columns=args[0], values=args[2])
    sea.heatmap(d, **kwargs)


def plot_heatmap(application: str, data, out_dir, level: int):
  fg = sea.FacetGrid(data[data.level == level], col='level', height=6)
  fg.map_dataframe(draw_heatmap, 'set-size', 'line-size', 'miss-pct', cmap='GnBu', annot=True, fmt='.2f', cbar=False)
  fg.axes[0,0].set(xlabel='set size (lines)', ylabel='line size (bytes)')
  fg.savefig(out_dir / f'{application}-scaling-L{level}.pdf', bbox_inches='tight')

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("Usage: non-contiguous.py <application>")
    sys.exit(1)

  script_dir = Path(os.path.dirname(os.path.realpath(__file__)))
  out_dir = script_dir / '../figures/scaling'
  os.makedirs(out_dir, exist_ok=True)

  application = sys.argv[1]
  data = read_data(application)

  data['line-size'] = pd.to_numeric(data.config.replace(r'L(\d+)-S(\d+)', r'\1', regex=True))
  data['set-size']  = pd.to_numeric(data.config.replace(r'L(\d+)-S(\d+)', r'\2', regex=True))
  data['miss-pct']  = data.misses / data.accesses * 100

  plot_heatmap(application, data, out_dir, 1)
  plot_heatmap(application, data, out_dir, 2)
