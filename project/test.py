import os
import subprocess
import pandas as pd

# Define the expected output file paths
OUTPUT_FILES = [
    './data/processed/renewable_energy_consumption_cleaned.csv',
    './data/processed/co2_emissions_cleaned.csv',
    './data/processed/data_cleaned.db'
]

# Function to run the ETL pipeline and capture its output
def execute_pipeline(script_name='./project/pipeline.py'):
    """
    Executes a Python script as a subprocess to run the ETL pipeline.
    Returns True if the script runs successfully; otherwise, False.
    """
    print("[INFO] Executing ETL pipeline...")
    try:
        result = subprocess.run(
            ['python', script_name],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("[INFO] Pipeline executed successfully.")
            print(result.stdout)
            return True
        else:
            print("[ERROR] Pipeline execution failed.")
            print(result.stderr)
            return False
    except FileNotFoundError:
        print(f"[ERROR] Script {script_name} not found.")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

# Function to validate the existence and content of files
def check_file_availability(file_list):
    """
    Validates that files in the provided list exist and are not empty.
    Returns True if all files meet the criteria; otherwise, False.
    """
    print("[INFO] Validating file availability...")
    missing_or_empty_files = [
        f for f in file_list if not os.path.exists(f) or os.path.getsize(f) == 0
    ]

    if missing_or_empty_files:
        print("[ERROR] The following files are missing or empty:")
        for file in missing_or_empty_files:
            print(f"  - {file}")
        return False

    print("[INFO] All files are present and non-empty:")
    for file in file_list:
        print(f"  - {file}")
    return True
# Function to check for missing values in the cleaned data files
def inspect_missing_values(file_paths):
    """
    Checks for missing values in CSV files and prints the results.
    Returns True if no missing values are found; otherwise, False.
    """
    print("[INFO] Checking files for missing data...")
    try:
        for file in file_paths:
            if file.endswith('.csv'):
                data = pd.read_csv(file)
                missing_values = data.isnull().sum().sum()
                if missing_values > 0:
                    print(f"[ERROR] Missing values found in file: {file}")
                    return False
        print("[INFO] No missing data in the inspected files.")
        return True
    except Exception as e:
        print(f"[ERROR] Error during missing value inspection: {e}")
        return False

# Main function to run all tests sequentially
def run_tests():
    """
    Executes the pipeline, validates file outputs, and inspects for missing data.
    """
    print("[INFO] Starting the test suite...")
    
    # Step 1: Run the ETL pipeline
    if not execute_pipeline():
        print("[FAILURE] Pipeline execution failed. Aborting tests.")
        return

    # Step 2: Validate output files
    if not check_file_availability(OUTPUT_FILES):
        print("[FAILURE] File validation failed. Aborting tests.")
        return

    # Step 3: Check for missing data in files
    csv_files = [file for file in OUTPUT_FILES if file.endswith('.csv')]
    if not inspect_missing_values(csv_files):
        print("[FAILURE] Missing data check failed.")
        return

    print("[SUCCESS] All tests passed successfully!")

if __name__ == "__main__":
    run_tests()
