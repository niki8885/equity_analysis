import os
import shutil


def clear_folders(*folders):
    """Deletes all files and subdirectories inside the specified folders."""
    for folder in folders:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # Delete file or symbolic link
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Delete folder and its contents
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
    print("Folders cleaned successfully!")
