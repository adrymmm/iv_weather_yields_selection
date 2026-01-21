## Research Question
How does variation in crop yields affect future planting decisions?

## Main Challenge
Crop yields are endogenous to planting decision. An appropriate instrument is needed to isolate a local average treatment effect.

## Data Sources
+ Level: United States **State-Level** Time-Series Data
+ Sources: 
  + **Agricultural**
    + USDA National Agricultural Statistics Service (NASS), Quick Stats API
    URL: https://quickstats.nass.usda.gov/
  + **Meteorological**
    + Source: NOAA National Centers for Environmental Information (NCEI), Global Historical Climatology Network – Daily (GHCN-Daily), Version 3
Download directory: https://www.ncei.noaa.gov/pub/data/ghcn/daily/
Primary dataset citation: Menne et al. (2012), DOI: 10.7289/V5D21VHZ

## Methods Employed:
+ LASSO Variable Selection with Grouped Cross-Validation
+ Two-Stage Least Square Regressions
+ Regression with Two-Way Fixed Effects
+ Nonlinear Feature Engineering
+ Overidentification and Exclusion Tests

## What We Learned
Across a broad set of instrumental variables, extreme June negative temperature shocks endogenously emerged as the most 
reliable source of identifying vatiation.

## Reproducibility
This repository is designed to be fully reproducible, subject to data availability constraints.

### Environment setup

Create a Python virtual environment and install dependencies:

```bash
pip install -r requirements.txt
pip install -r requirements-jupyter.txt
```

### Data Availability 
Raw data files are not included. Agricultural data can be extracted through the API by running the Jupyter notebook.
Meteorological data is sourced on its respective notebook. The name of the file is _ghcnd_hcn.tar_