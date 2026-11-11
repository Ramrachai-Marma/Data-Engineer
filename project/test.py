"""Run the ETL pipeline and validate its generated CSV and SQLite outputs."""

import logging
import sqlite3
import subprocess
import sys
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_FILES = [
    DATA_DIR / "renewable_energy_consumption_cleaned.csv",
    DATA_DIR / "co2_emissions_cleaned.csv",
    DATA_DIR / "data_cleaned.db",
]
TABLES = {
    "renewable_energy_consumption_data",
    "co2_emissions_data",
}

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def execute_pipeline() -> bool:
    """Run the ETL with the current Python interpreter."""
    pipeline_path = PROJECT_DIR / "project" / "pipeline.py"
    logger.info("Executing ETL pipeline.")
    result = subprocess.run(
        [sys.executable, str(pipeline_path)],
        cwd=PROJECT_DIR,
        check=False,
        text=True,
        capture_output=True,
    )
    if result.stdout:
        logger.info("%s", result.stdout.rstrip())
    if result.returncode:
        logger.error("Pipeline failed:\n%s", result.stderr.rstrip())
        return False
    return True


def validate_output_files() -> bool:
    """Ensure every expected output exists and contains data."""
    invalid_files = [
        path for path in OUTPUT_FILES if not path.is_file() or path.stat().st_size == 0
    ]
    if invalid_files:
        logger.error("Missing or empty output files: %s", ", ".join(map(str, invalid_files)))
        return False
    return True


def validate_csv_files() -> bool:
    """Ensure each output CSV has records and no missing values."""
    for path in OUTPUT_FILES:
        if path.suffix != ".csv":
            continue
        try:
            data = pd.read_csv(path)
        except (OSError, pd.errors.ParserError, UnicodeDecodeError) as error:
            logger.error("Could not read %s: %s", path, error)
            return False
        if data.empty:
            logger.error("CSV output contains no records: %s", path)
            return False
        if data.isna().any().any():
            logger.error("Missing values found in %s", path)
            return False
    return True


def validate_database() -> bool:
    """Ensure the SQLite database contains both non-empty indicator tables."""
    database_path = OUTPUT_FILES[-1]
    try:
        with sqlite3.connect(database_path) as connection:
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                )
            }
            if not TABLES.issubset(tables):
                logger.error("SQLite database is missing tables: %s", TABLES - tables)
                return False
            for table in sorted(TABLES):
                count = connection.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
                if count == 0:
                    logger.error("SQLite table is empty: %s", table)
                    return False
    except sqlite3.Error as error:
        logger.error("Could not validate SQLite database: %s", error)
        return False
    return True


def main() -> int:
    if not execute_pipeline():
        return 1
    if not validate_output_files():
        return 1
    if not validate_csv_files() or not validate_database():
        return 1
    logger.info("All ETL output checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
