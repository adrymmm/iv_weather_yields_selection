# IV Weather & Yield Selection

Instrumental variable analysis of how crop yield shocks affect future planting decisions across US states, using weather variation as instruments. The core challenge is that crop yields are endogenous to planting decisions: farmers respond to expected yields, not just realised ones. Weather shocks provide exogenous variation in yields that is plausibly unrelated to the planting decision directly.

## Research Question

Does a positive yield shock in the current year suppress planted area in the following year, consistent with a supply adjustment mechanism?

## Data

US state-level panel data across two sources:

| Source | Variable | Link |
|---|---|---|
| USDA NASS Quick Stats API | Crop yield, area harvested | https://quickstats.nass.usda.gov/ |
| NOAA GHCN-Daily (Menne et al., 2012) | Monthly temperature, precipitation | https://www.ncei.noaa.gov/pub/data/ghcn/daily/ |

Weather variables are standardised within state and month to construct z-scored instruments ($Z_{\text{temp},m}$, $Z_{\text{prcp},m}$) for $m = 1, \ldots, 12$.

## Model

**First stage** - instrument relevance: weather shocks $\mathbf{Z}$ predict log crop yield

$$\log y_{it} = \alpha_i + \lambda_t + \mathbf{Z}_{it}'\pi + \nu_{it}$$

**Second stage** - causal effect of yield on next-year planted area:

$$\log a_{i,t+1} = \alpha_i + \lambda_t + \beta \widehat{\log y_{it}} + \varepsilon_{it}$$

where $\alpha_i$ and $\lambda_t$ are state and year fixed effects, and $\beta$ is the causal elasticity of interest. Standard errors clustered at the state level throughout.

## Pipeline

**`01_crop_yield_clean.ipynb`** - Fetches crop yield and area harvested data via the USDA NASS API. Constructs log yield and log area harvested lead variables.

**`02_weather_clean.ipynb`** - Processes NOAA GHCN-Daily station data, aggregates to state-month level, and constructs standardised temperature and precipitation instruments.

**`03_fe_model.ipynb`** - Runs two-way FE regression of log yield on all 24 candidate instruments (12 months, temperature and precipitation). Applies LASSO with grouped cross-validation (GroupKFold, groups = state) to select relevant instruments from the demeaned data. Runs stability selection across 50 random subsample draws (dropping 5 years per run), retaining instruments selected in 80% or more of runs, yielding 13 stable instruments.

**`04_nonlinear_search.ipynb`** - Expands the instrument set to 130 features via nonlinear transformations (polynomials, hinge functions at quartiles, absolute values). Re-applies LASSO and stability selection (200 bootstrap draws, 70% entity subsample). Ranks instruments by first-stage F-statistic, stress-tests the exclusion restriction by adding adjacent month controls, and estimates the final just-identified 2SLS. Applies double LASSO inference (Belloni, Chernozhukov and Hansen, 2012) by partialling out the remaining nonlinear weather controls from outcome, treatment, and instrument separately before running IV on the residuals, correcting for post-selection inference bias.

## Key Findings

**Instrument selection:** June temperature negative shocks (below 75th percentile hinge) emerged as the strongest instrument after LASSO and stability selection, with a naive first-stage F-statistic of 23.4 and partial $R^2 = 0.015$. July cubic temperature was the most powerful individual instrument by F-statistic ($F = 34.8$).

**Causal estimate:** The preferred double LASSO estimate gives $\beta = -0.865$ (SE = 0.446, $p = 0.053$), implying a 1% increase in current-year yield reduces planted area the following year by approximately 0.86%, conditional on state and year fixed effects. The naive post-selection IV estimate is $\beta = -1.039$ (SE = 0.559, $p = 0.063$). Both specifications agree in direction, magnitude, and significance level. The negative supply response is consistent with rational farmer adjustment: a positive yield shock lowers expected scarcity, reducing the incentive to expand plantings.

**Double LASSO first stage:** Partialling out the remaining weather controls while preserving the full June temperature family as the instrument raises the first-stage F to 46.5, confirming instrument strength is not an artefact of shared variation with the control set.

**Exclusion restriction:** Stress-testing by adding adjacent month weather controls leaves coefficients stable across all three top instruments (June negative hinge: baseline $\beta = -1.039$, stress $\beta = -0.820$), supporting the validity of the exclusion restriction.

**Overidentification:** The Wooldridge score test rejects the null of no overidentification ($\chi^2 = 48.1$, $p = 0.0001$) on the full instrument set, motivating the just-identified final specification.

## Repository Structure
```
├── notebooks/
│   ├── 01_crop_yield_clean.ipynb
│   ├── 02_weather_clean.ipynb
│   ├── 03_fe_model.ipynb
│   └── 04_nonlinear_search.ipynb
├── src/
│   └── utils/
│       ├── init.py
│       ├── demeaning.py
│       ├── feature_eng.py
│       └── iv_helpers.py
├── data/
└── requirements.txt
```

## Requirements

```bash
pip install -r requirements.txt
```

## Reproducibility

Raw meteorological data requires downloading `ghcnd_hcn.tar` from the NOAA link above (omitted due to file size). Agricultural data is fetched via the USDA NASS API; set the environment variable `NASS_API_KEY` in a `.env` file in the project root (key available at https://quickstats.nass.usda.gov/api).

Run notebooks in numbered order from the project root.