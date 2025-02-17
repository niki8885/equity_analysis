import os
import shutil
import glob
import pandas as pd

def clear_folders(*folders):
    """Deletes the specified folders completely and recreates them empty."""
    for folder in folders:
        abs_path = os.path.abspath(folder)  # Get absolute path to avoid issues
        try:
            if os.path.exists(abs_path):
                shutil.rmtree(abs_path)  # Remove the folder and all its contents
                print(f"Deleted: {abs_path}")
            os.makedirs(abs_path, exist_ok=True)  # Recreate the folder
            print(f"Recreated: {abs_path}")
        except Exception as e:
            print(f"Failed to reset {abs_path}: {e}")


def clear_working_folders():
    """Completely removes and recreates the 'data' folder and subdirectories (outside the package)."""
    base_data_folder = "../data"  # Make sure it's outside 'mypackage/'
    subfolders = ["plots", "financial_data", "reports", "raw_data"]

    # Ensure the main 'data' folder is completely reset
    clear_folders(base_data_folder)

    # Recreate all subdirectories inside 'data'
    for subfolder in subfolders:
        path = os.path.join(base_data_folder, subfolder)
        os.makedirs(path, exist_ok=True)
        print(f"Created: {path}")

    print("Data folder structure recreated successfully!")


def price(ticker, method = "current"):
    """Loads the latest available price from a file matching {ticker}_analysis.csv"""
    file_pattern = f"../data/financial_data/{ticker}_analysis.csv"
    files = glob.glob(file_pattern)

    if not files:
        raise FileNotFoundError(f"No file matching {ticker}_analysis.csv found in {os.path.dirname(file_pattern)}")

    # Select the first matching file (you can modify this logic if needed)
    file_path = files[0]
    data = pd.read_csv(file_path)

    match method:
        case "current":
            price = data[method].dropna().iloc[-1]
            print(f"Current price of {ticker}: {price}")
        case "high":
            price = data[method].dropna().iloc[-1]
            print(f"Highest price of {ticker}: {price}")
        case "low":
            price = data[method].dropna().iloc[-1]
            print(f"Lowest price of {ticker}: {price}")
        case "mean":
            price = data[method].dropna().iloc[-1]
            print(f"Mean price of {ticker}: {price}")
        case "median":
            price = data[method].dropna().iloc[-1]
            print(f"Median price of {ticker}: {price}")
        case _:
            raise ValueError(f"Invalid method: {method}")

    return price
