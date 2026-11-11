# Project Plan: Renewable Energy and CO2 Indicators

## Research question

How do renewable-energy consumption and the selected CO2 indicator vary across the configured North American, Central American, and Caribbean countries and territories from 2015 through 2021?

The analysis is exploratory. Comparing these indicators can describe patterns and associations, but does not establish that renewable-energy consumption causes changes in emissions.

## Data sources

| Dataset | World Bank indicator | Metadata |
|---|---|---|
| Renewable energy consumption | `EG.FEC.RNEW.ZS` | <https://data.worldbank.org/indicator/EG.FEC.RNEW.ZS> |
| CO2 emissions | `EN.GHG.CO2.PI.MT.CE.AR5` | <https://data.worldbank.org/indicator/EN.GHG.CO2.PI.MT.CE.AR5> |

The pipeline downloads the corresponding CSV archives through the World Bank API. It selects the countries and years configured in `pipeline.py`, reshapes observations into long form, and writes CSV and SQLite outputs.

## Work plan

1. Define the research question, scope, and data-quality checks.
2. Download and inspect both indicator datasets.
3. Filter the selected locations and study years; document missing observations.
4. Produce cleaned CSV and SQLite outputs with an automated pipeline.
5. Test transformations and output structure using offline unit tests.
6. Analyze trends and limitations; avoid causal claims unsupported by the data.
7. Publish the report with source attribution and reproducibility instructions.
