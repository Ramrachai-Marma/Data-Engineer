# Renewable Energy and CO2 Data Pipeline

A small data-engineering project that downloads two World Bank indicators, filters them to selected countries and territories across North America, Central America, and the Caribbean, reshapes annual observations, and exports cleaned data as CSV and SQLite.

The pipeline supports an exploratory question about the relationship between renewable energy use and CO2 emissions. It prepares the datasets; it does not, by itself, establish a causal relationship.

## Data sources

| Indicator | World Bank code | Source |
|---|---|---|
| Renewable energy consumption | `EG.FEC.RNEW.ZS` | [World Bank indicator page](https://data.worldbank.org/indicator/EG.FEC.RNEW.ZS) |
| CO2 emissions | `EN.GHG.CO2.PI.MT.CE.AR5` | [World Bank indicator page](https://data.worldbank.org/indicator/EN.GHG.CO2.PI.MT.CE.AR5) |

The current pipeline selects observations from 2015 through 2021. The source data is downloaded at runtime, so execution requires internet access.

## What the pipeline does

1. Downloads each indicator archive from the World Bank API and reads its data CSV.
2. Selects the configured country/territory records and years.
3. Converts the year columns into a long-form `Year` / `Value` representation.
4. Writes one cleaned CSV per indicator and stores the corresponding tables in a SQLite database.

## Setup and run

Run these commands from the repository root (the directory containing `project/`):

```bash
python -m venv .venv
```

Activate the environment (`.\.venv\Scripts\Activate.ps1` in PowerShell, or `source .venv/bin/activate` on macOS/Linux), then install dependencies:

```bash
python -m pip install -r project/requirements.txt
```

Run the ETL once (this requires internet access):

```bash
python project/pipeline.py
```

The integration validation script reruns the ETL before checking its output files:

```bash
python project/test.py
```

Run the offline unit tests (no API keys or network required):

```bash
python -m unittest discover -s project/tests -v
```

GitHub Actions runs the offline unit tests on pushes and pull requests. The integration pipeline is intentionally not run in CI because it downloads data from the World Bank service.

## Outputs

The pipeline creates `data/processed/` in this project directory:

- `renewable_energy_consumption_cleaned.csv`
- `co2_emissions_cleaned.csv`
- `data_cleaned.db` - SQLite tables `renewable_energy_consumption_data` and `co2_emissions_data`

Generated files are not included in the repository by default.

## Repository guide

- `project/pipeline.py` - Download, transform, and export steps
- `project/test.py` - Pipeline and output checks
- `project/project-plan.md` - Project plan
- `project/Analysis_Report__.pdf` - Analysis report
- `project/Data_Report.pdf` - Data report
- `exercises/` - Jayvee course exercises and example databases
- `.github/workflows/` - Existing GitHub Actions workflows

## License

See [`LICENSE`](LICENSE). Review the World Bank's current data terms before redistributing source or derived datasets.
