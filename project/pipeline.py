

import os
import zipfile
import requests
import pandas as pd
import sqlite3
from io import BytesIO

data_directory = r"C:\Users\ramra\MADE_LAB\made-Ramrachai-Marma\project\data\processed"


if not os.path.exists(data_directory):
    os.makedirs(data_directory)

north_american_countries = [
    "Canada", "United States", "Mexico", "Bermuda", "Bahamas, The",
    "Barbados", "Cuba", "Haiti", "Dominican Republic", "Jamaica",
    "Trinidad and Tobago", "Saint Kitts and Nevis", "Antigua and Barbuda",
    "Saint Lucia", "Saint Vincent and the Grenadines", "Grenada", "Belize",
    "Panama", "Costa Rica", "El Salvador", "Honduras", "Nicaragua",
    "Guatemala"
]

url_renewable_energy_consumption = "https://api.worldbank.org/v2/en/indicator/EG.FEC.RNEW.ZS?downloadformat=csv"
url_co2_emissions = "https://api.worldbank.org/v2/en/indicator/EN.GHG.CO2.PI.MT.CE.AR5?downloadformat=csv"


def download_and_extract_zip(url, output_dir):
    response = requests.get(url)
    if response.status_code == 200:
        with zipfile.ZipFile(BytesIO(response.content)) as z:
            z.extractall(output_dir)
            print(f"Extracted files to {output_dir}")
            csv_files = [f for f in z.namelist() if f.endswith(".csv") and "Metadata" not in f]
            return [os.path.join(output_dir, f) for f in csv_files]
    else:
        print(f"Failed to download data from {url}.")
        return []


def clean_and_reshape_data(file_path, countries, years):
    df = pd.read_csv(file_path, skiprows=4)
    print(f"Loaded file: {file_path}")
    print("Columns in dataset:", df.columns)
    
    required_columns = ["Country Name", "Country Code"] + years
    for col in required_columns:
        if col not in df.columns:
            print(f"Warning: Column '{col}' not found in the dataset. Available columns: {list(df.columns)}")
            return pd.DataFrame()  
    
    df_filtered = df[df["Country Name"].isin(countries)][["Country Name", "Country Code","Indicator Name"] + years]
    
    df_long = df_filtered.melt(
        id_vars=["Country Name", "Country Code","Indicator Name"],
        var_name="Year",
        value_name="Value"
    )
    return df_long


def export_to_sqlite(df, table_name, db_path):
    if df.empty:
        print(f"Skipped saving table '{table_name}' due to empty DataFrame.")
        return
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Saved table '{table_name}' to SQLite database at {db_path}.")


renewable_energy_consumption_files = download_and_extract_zip(url_renewable_energy_consumption, data_directory)


co2_emissions_files = download_and_extract_zip(url_co2_emissions, data_directory)


years = [str(year) for year in range(2015, 2022)]


if renewable_energy_consumption_files:
    renewable_energy_consumption_cleaned = clean_and_reshape_data(
        renewable_energy_consumption_files[0], north_american_countries, years
    )
    if not renewable_energy_consumption_cleaned.empty:
        renewable_energy_consumption_cleaned.to_csv(
            os.path.join(data_directory, "renewable_energy_consumption_cleaned.csv"), index=False
        )
        print("Cleaned renewable energy consumption data saved as CSV.")
        export_to_sqlite(
            renewable_energy_consumption_cleaned,
            "renewable_energy_consumption_data",
            os.path.join(data_directory, "data_cleaned.db")  # Save database here
        )


if co2_emissions_files:
    co2_emissions_cleaned = clean_and_reshape_data(
        co2_emissions_files[0], north_american_countries, years
    )
    if not co2_emissions_cleaned.empty:
        co2_emissions_cleaned.to_csv(
            os.path.join(data_directory, "co2_emissions_cleaned.csv"), index=False
        )
        print("Cleaned CO2 emissions data saved as CSV.")
        export_to_sqlite(
            co2_emissions_cleaned,
            "co2_emissions_data",
            os.path.join(data_directory, "data_cleaned.db")  # Save database here
        )