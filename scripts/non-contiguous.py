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
    next_data = pd.read_csv(f'../data/{application}/bundles-{w}.csv')
    next_data['svewidth'] = w
    data = data.append(next_data, ignore_index=True)

  return data

def plot_lines_touched_single(application: str, data, out_dir, line_size: int):
  data['lines'] = pd.to_numeric(np.ceil(data.delta * 8 / line_size), downcast='integer') + 1
  data.lines.clip(upper=data.components, inplace=True)
  data.lines.clip(upper=data.svewidth/8, inplace=True)

  fig, ax = plt.subplots()

  graphdata = data[(data['count'] > 2)]
  sea.violinplot(x='lines', y='svewidth', data=graphdata, ax=ax,
    cut=0, palette='colorblind', orient='h', scale='count', inner='quartile', bw=.25)

  plt.xticks(range(1,max(graphdata.lines)+1))
  ax.set_xlabel('cache lines touched')
  ax.set_ylabel('svewidth (bits)')

  fig.savefig(out_dir / f'{application}-non-countiguous-{line_size}.pdf', bbox_inches='tight')

def plot_lines_touched_both(application: str, data, out_dir):
  bothdata = data[(data['count'] > 2)].copy()
  bothdata['A64FX'] = pd.to_numeric(np.ceil(data.delta * 8 / 256), downcast='integer') + 1
  bothdata['TX2']   = pd.to_numeric(np.ceil(data.delta * 8 / 64), downcast='integer') + 1
  for col in ['A64FX','TX2']:
      bothdata[col].clip(upper=data.components, inplace=True)
      # bothdata[col].clip(upper=data.svewidth/8, inplace=True)

  melted = bothdata.drop(columns=['components','delta','lines']).melt(id_vars='svewidth', value_vars=['A64FX','TX2'],
                                                                      var_name='config', value_name='count')

  fig, ax = plt.subplots()
  sea.violinplot(x='count', y='svewidth', hue='config', hue_order=['TX2','A64FX'], split=True, data=melted, ax=ax,
                      cut=0, palette='colorblind', orient='h', scale='count', inner='point', bw=.2)

  ax.set_xlabel('cache lines touched')
  ax.set_ylabel('sve width (bits)')
  ax.legend()
  ax.set_xscale('log', basex=2)
  ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda x, _: '{:.16g}'.format(x)))

  fig.savefig(out_dir / f'{application}-non-countiguous-both.pdf', bbox_inches='tight')


if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("Usage: non-contiguous.py <application>")
    sys.exit(1)

  script_dir = Path(os.path.dirname(os.path.realpath(__file__)))
  out_dir = script_dir / '../figures/non-contiguous'
  os.makedirs(out_dir, exist_ok=True)

  application = sys.argv[1]
  data = read_data(application)

  sea.set(style='whitegrid')
  plot_lines_touched_single(application, data, out_dir, 64)
  plot_lines_touched_single(application, data, out_dir, 256)

  plot_lines_touched_both(application, data, out_dir)
