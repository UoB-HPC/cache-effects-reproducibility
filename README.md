# Reproducibility

This repository contains reproducibility data and scripts for the EAHPC-2020 paper _The Effects of Wide Vector Operations on Processor Caches_.

## Data

Data is found in the `data` folder, in CSV format.
There is a subfolder for each of the applications studied.

## Visualisations

The `scripts` folder contains Python scripts to produce graphs as included in the paper.
All graphs can be produced for all applications, at both the first and second levels of cache.

The corespondence between the graphs in the paper and the scripts in this repository is as follows:

* `cache-parameters.py` produces heatmaps as presented in Section IV-A
* `sve-length.py` produces bar charts as presented in Section IV-B
* `lifetimes.py` produces distribution grids as presented in Section IV-C
* `non-contiguous.py` produces violin plots as presented in Section IV-D

### Running the scripts

Python 3.7+ is required to run the scripts.
The visualisations are produced using [PANDAS](https://pandas.pydata.org/) and [Seaborn](https://seaborn.pydata.org/).
The dependencies can be installed with `pip` by running the following command in the `scripts` directory:

    pip install -r requirements.txt

All the scripts have to be run from inside the `scripts` directory (because they expect the data to be found in `../data`).
They have the same interface:

    ./<graph>.py <application>

...where `<graph>` is the name of one of the scripts above and `<application>` is one of the choices in the `data` directory:

* `cloverleaf`
* `mega-sweep`
* `minifmm`
* `stream`
