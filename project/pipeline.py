"""Download and reshape World Bank renewable-energy and CO2 indicators."""

import logging
import sqlite3
import zipfile
from contextlib import closing
from io import BytesIO
from pathlib import Path
from typing import Sequence

import pandas as pd
import requests

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data" / "processed"
YEARS = [str(year) for year in range(2015, 2022)]
COUNTRIES = [
    "Canada", "United States", "Mexico", "Bermuda", "Bahamas, The",
    "Barbados", "Cuba", "Haiti", "Dominican Republic", "Jamaica",
    "Trinidad and Tobago", "Saint Kitts and Nevis", "Antigua and Barbuda",
    "Saint Lucia", "Saint Vincent and the Grenadines", "Grenada", "Belize",
    "Panama", "Costa Rica", "El Salvador", "Honduras", "Nicaragua",
    "Guatemala",
]
INDICATORS = {
    "renewable_energy_consumption": "EG.FEC.RNEW.ZS",
    "co2_emissions": "EN.GHG.CO2.PI.MT.CE.AR5",
}

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def download_indicator_csv(indicator_code: str) -> pd.DataFrame:
    """Download an indicator archive and read its data CSV."""
    url = (
        "https://api.worldbank.org/v2/en/indicator/"
        f"{indicator_code}?downloadformat=csv"
    )
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    with zipfile.ZipFile(BytesIO(response.content)) as archive:
        csv_names = [
            name
            for name in archive.namelist()
            if name.lower().endswith(".csv")
            and "metadata" not in name.lower()
            and name.rsplit("/", 1)[-1].startswith("API_")
        ]
        if not csv_names:
            raise ValueError(f"No indicator data CSV found in the archive for {indicator_code}.")
        if len(csv_names) > 1:
            raise ValueError(f"Expected one indicator CSV for {indicator_code}, found {len(csv_names)}.")
        with archive.open(csv_names[0]) as csv_file:
            return pd.read_csv(csv_file, skiprows=4)


def clean_and_reshape_data(
    frame: pd.DataFrame,
    countries: Sequence[str] = COUNTRIES,
    years: Sequence[str] = YEARS,
) -> pd.DataFrame:
    """Filter country/year observations and reshape them into long form."""
    required_columns = ["Country Name", "Country Code", "Indicator Name", *years]
    missing_columns = [column for column in required_columns if column not in frame.columns]
    if missing_columns:
        raise ValueError(
            "World Bank data is missing required columns: "
            f"{', '.join(missing_columns)}"
        )

    filtered = frame.loc[
        frame["Country Name"].isin(countries),
        required_columns,
    ]
    long_form = filtered.melt(
        id_vars=["Country Name", "Country Code", "Indicator Name"],
        var_name="Year",
        value_name="Value",
    )
    return long_form.dropna(subset=["Value"]).reset_index(drop=True)


def save_outputs(
    data: pd.DataFrame,
    name: str,
    database_path: Path,
) -> None:
    """Save one indicator as CSV and as a SQLite table."""
    if data.empty:
        raise ValueError(f"No observations found for {name}; refusing to write empty outputs.")

    csv_path = DATA_DIR / f"{name}_cleaned.csv"
    data.to_csv(csv_path, index=False)
    with closing(sqlite3.connect(database_path)) as connection:
        with connection:
            data.to_sql(f"{name}_data", connection, if_exists="replace", index=False)
    logger.info("Saved %s rows to %s and SQLite table %s_data", len(data), csv_path, name)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    database_path = DATA_DIR / "data_cleaned.db"

    for name, indicator_code in INDICATORS.items():
        logger.info("Downloading World Bank indicator %s", indicator_code)
        source_data = download_indicator_csv(indicator_code)
        cleaned_data = clean_and_reshape_data(source_data)
        save_outputs(cleaned_data, name, database_path)


if __name__ == "__main__":
    main()
