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
```

### Data Availability 
Raw meteorogical data is missing the tar file _ghcnd_hcn.tar_. This was omitted due to size but the source link can be 
found in the notebook _02_weather_clean_. Agricultural data can be extracted through the API by running the Jupyter notebook.

### API Access
Visit https://quickstats.nass.usda.gov/api and click on *Request API KEY*. You will receive the key in the specified email.
In *01_crop_yield_clean* set the enviroment variable *NASS_API_KEY* to your personal API key.