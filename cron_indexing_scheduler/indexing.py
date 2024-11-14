import os
import yaml
from pathlib import Path
from datetime import datetime

def count_changes(existing_files, current_files):
    new_files = list(set(current_files) - set(existing_files))
    deleted_files = list(set(existing_files) - set(current_files))

    return {
        "new_files": new_files,
        "deleted_files": deleted_files
    }

def label_changes(changes):
    labeled_changes = {
        "new_files": {},
        "deleted_files": {},
        "modified_files": {}
    }

    for change_type, change_files in changes.items():
        for file_path in change_files:
            parts = file_path.split(os.path.sep)  # Split the file path into parts
            current_dict = labeled_changes[change_type]

            # Traverse the parts to create nested dictionaries
            for part in parts[:-1]:
                current_dict = current_dict.setdefault(part, {})

            # Add the file to the nested dictionary
            current_dict[parts[-1]] = True

    return labeled_changes

def update_index_file(update_file_path, files):
    with open(update_file_path, "w") as f:
        yaml.dump({"files": files}, f)


def get_all_files(tracked_directory):
    all_files = []

    # Get all files within the tracked directory (recursively)
    for file_path in Path(tracked_directory).rglob("*"):
        if file_path.is_file():
            # Convert to a string and make it relative to the tracked directory
            relative_path = str(file_path.relative_to(tracked_directory))
            all_files.append(relative_path)

    return all_files


def main():
    print("executing indexing.py")
    tracked_directory = "./local_media_production"
    index_file = "./local_media_production/index.update.yml"


    # Get all files within each subdirectory
    all_files = get_all_files(tracked_directory)
    
    print(f"tracked directory: {tracked_directory}")
    print(f"tracked files : {all_files}")
    print(f"tracked index file {index_file}")

    # Check for changes in the tracked directory
    if os.path.exists(index_file):
        with open(index_file, "r") as f:
            try:
                index_data = yaml.safe_load(f) or {}
                existing_files = index_data.get("files", [])
            except yaml.YAMLError as e:
                print(f"Error reading YAML data: {e}")
                # Assume an upload is needed in case of an error
                existing_files = []

        # Calculate changes
        changes = count_changes(existing_files, all_files)

        # Label changes
        labeled_changes = label_changes(changes)

        # Update the index file
        update_index_file(index_file, labeled_changes)

        print("Changes:", changes)
        print("Labeled Changes:", labeled_changes)


if __name__ == "__main__":
    main()
