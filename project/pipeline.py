# /project/pipeline.py

import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

# Base directory of your project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directories
DATA_DIR = os.path.join(BASE_DIR, 'data')  # Changed here
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')

# Kaggle dataset identifier
KAGGLE_DATASET = 'rizwanash/electric-vehicle-population-data'

def create_data_dirs():
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

def download_dataset():
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(KAGGLE_DATASET, path=RAW_DATA_DIR, unzip=True)

def load_data():
    csv_file = os.path.join(RAW_DATA_DIR, 'Electric_Vehicle_Population_Data.csv')
    df = pd.read_csv(csv_file)
    return df

def clean_data(df):
    # Handle missing values
    df = df.dropna()

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Convert data types if necessary
    df['model_year'] = df['model_year'].astype(int)

    # Remove duplicates
    df = df.drop_duplicates()

    return df

def save_data(df):
    # Save as CSV
    processed_csv = os.path.join(PROCESSED_DATA_DIR, 'electric_vehicle_population_data_cleaned.csv')
    df.to_csv(processed_csv, index=False)

    # Save as SQLite database
    from sqlalchemy import create_engine
    db_path = os.path.join(PROCESSED_DATA_DIR, 'electric_vehicle_data.db')
    engine = create_engine(f'sqlite:///{db_path}')
    df.to_sql('electric_vehicles', con=engine, if_exists='replace', index=False)

def main():
    create_data_dirs()
    download_dataset()
    df = load_data()
    df_cleaned = clean_data(df)
    save_data(df_cleaned)
    print("Data pipeline executed successfully.")

if __name__ == '__main__':
    main()
