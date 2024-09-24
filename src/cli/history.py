import json
import os
import typer
from datetime import datetime
from config import HISTORY_FILE, HISTORY_VERSION, DATABASE_STORAGE_DIR


# Creates a new history file if it doesn't exist
def history_create():
    history_path = os.path.join(os.path.dirname(__file__), HISTORY_FILE)

    # Check if history file already exists
    if not os.path.exists(history_path):
        history_data = {"version": HISTORY_VERSION, "databases": [], "current_db": ""}

        # Write the initial history data to the file
        with open(history_path, "w") as f:
            json.dump(history_data, f, indent=4)

        print(f"History file created: '{history_path}'")
    else:
        print(f"History file already exists: '{history_path}'")


# Generate the next available database filename based on the date and existing files
def get_next_db_filename():
    history_path = os.path.join(os.path.dirname(__file__), HISTORY_FILE)

    if os.path.exists(history_path):
        with open(history_path, "r") as f:
            history_data = json.load(f)
    else:
        history_create()
        with open(history_path, "r") as f:
            history_data = json.load(f)

    today_date = datetime.now().strftime("%Y-%m-%d")
    existing_files_today = [
        db["filename"]
        for db in history_data["databases"]
        if db["filename"].startswith(today_date)
    ]

    # Calculate the copy number based on existing files
    copy_number = len(existing_files_today) + 1
    db_filename = f"{today_date}-{copy_number}.ttl"

    return db_filename


# Adds a new database entry to the history file and marks it as the current one
def history_add_db(filename):
    history_path = os.path.join(os.path.dirname(__file__), HISTORY_FILE)

    if os.path.exists(history_path):
        with open(history_path, "r") as f:
            history_data = json.load(f)
    else:
        history_create()
        with open(history_path, "r") as f:
            history_data = json.load(f)

    history_data["databases"].append(
        {
            "filename": filename,
            "created_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        }
    )

    history_data["current_db"] = filename
    with open(history_path, "w") as f:
        json.dump(history_data, f, indent=4)

    print(f"Added new DB to history file: '{filename}', marked as current DB.")
    return filename


# Returns the current database filename and its creation date
def get_current_db():
    history_path = os.path.join(os.path.dirname(__file__), HISTORY_FILE)

    if os.path.exists(history_path):
        with open(history_path, "r") as f:
            history_data = json.load(f)

        current_db = history_data.get("current_db", None)

        # Find the current database entry and its creation date
        if current_db:
            for db_entry in history_data.get("databases", []):
                if db_entry.get("filename") == current_db:
                    creation_date = db_entry.get("created_at")
                    return current_db, creation_date

        return current_db, None  # Return None if creation date is not found

    else:
        print("Error: History file does not exist. Creating one...")
        history_create()
        return None


# Retrieves all databases
def get_all_databases():
    history_path = os.path.join(os.path.dirname(__file__), HISTORY_FILE)

    if os.path.exists(history_path):
        with open(history_path, "r") as f:
            history_data = json.load(f)

        return history_data.get("databases", [])

    return []


# Update the current database in the history file
def update_current_db(new_db):
    history_path = os.path.join(os.path.dirname(__file__), HISTORY_FILE)

    if os.path.exists(history_path):
        with open(history_path, "r") as f:
            history_data = json.load(f)

        history_data["current_db"] = new_db

        with open(history_path, "w") as f:
            json.dump(history_data, f, indent=4)


# Delete a database from the history file
def delete_db(filename):
    history_path = os.path.join(os.path.dirname(__file__), HISTORY_FILE)
    db_file_path = os.path.join(DATABASE_STORAGE_DIR, filename)

    if os.path.exists(history_path):
        with open(history_path, "r") as f:
            history_data = json.load(f)

        # Remove the database from the history list
        history_data["databases"] = [
            db for db in history_data["databases"] if db["filename"] != filename
        ]

        with open(history_path, "w") as f:
            json.dump(history_data, f, indent=4)

        # Delete the actual file from the storage directory
        if os.path.exists(db_file_path):
            os.remove(db_file_path)
            typer.echo(f">> Database '{db_file_path}' deleted successfully.")
        else:
            typer.echo(
                f"Error: File '{db_file_path}' does not exist or has already been deleted."
            )
    else:
        typer.echo(f"Error: History file '{history_path}' does not exist.")
