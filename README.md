# Happy Cows

## Project Overview

This repository is intended for the analysis of milk production data, collected from a small Pennsylvania dairy farm.  For additional information check out the [project overview](references/OVERVIEW.md).

## Structure

The directory structure of your new project looks like this:

```
├── LICENSE
├── README.md          <- The top-level README
├── config.yml         <- Template Configuration File
│
├── data
│   ├── processed      <- The final data sets.
│   └── raw            <- The original, immutable data dump.
│
├── notebooks          <- Jupyter notebooks.
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
└── scripts            <- Scripts utilized in data manipulation.
```

## Setup

Install dependencies

``` python
python scripts/get_requirements.py
```

Download raw data

``` python
python scripts/get_data.py
```

Generate database from raw data

``` python
python scripts/load_database.py
```

Calculate days since calving

``` python
python scripts/add_days_since_calving.py
```