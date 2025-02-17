import os
import shutil


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
