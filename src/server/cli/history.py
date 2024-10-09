import json
import os
import typer
from datetime import datetime
from cli.config import HISTORY_FILE, HISTORY_VERSION, DATABASE_STORAGE_DIR


# Creates a new history file if it doesn't exist
def history_create():
    if os.path.exists(HISTORY_FILE):
        print(f"History file already exists: '{HISTORY_FILE}'")
        return

    history_data = {"version": HISTORY_VERSION, "databases": [], "current_db": ""}
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history_data, f, indent=4)

    print(f"History file created: '{HISTORY_FILE}'")


# Generate the next available database filename based on the date and existing files
def get_next_db_filename():
    if not os.path.exists(HISTORY_FILE):
        history_create()

    with open(HISTORY_FILE, "r") as f:
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
    if not os.path.exists(HISTORY_FILE):
        history_create()

    with open(HISTORY_FILE, "r") as f:
        history_data = json.load(f)

    history_data["databases"].append(
        {
            "filename": filename,
            "created_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        }
    )

    history_data["current_db"] = filename
    with open(HISTORY_FILE, "w") as f:
        json.dump(history_data, f, indent=4)

    print(f"Added new DB to history file: '{filename}', marked as current DB.")
    return filename


# Returns the current database filename and its creation date
def get_current_db():
    if not os.path.exists(HISTORY_FILE):
        print("Error: History file does not exist. Creating one...")
        history_create()
        return None, None

    with open(HISTORY_FILE, "r") as f:
        history_data = json.load(f)

    current_db = history_data.get("current_db", None)

    # Find the current database entry and its creation date
    if current_db:
        for db_entry in history_data.get("databases", []):
            if db_entry.get("filename") == current_db:
                creation_date = db_entry.get("created_at")
                return current_db, creation_date

    return current_db, None  # Return None if creation date is not found


# Retrieves all databases
def get_all_databases():
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as f:
        history_data = json.load(f)
    return history_data.get("databases", [])


# Update the current database in the history file
def update_current_db(new_db):
    if not os.path.exists(HISTORY_FILE):
        return

    with open(HISTORY_FILE, "r") as f:
        history_data = json.load(f)

    history_data["current_db"] = new_db

    with open(HISTORY_FILE, "w") as f:
        json.dump(history_data, f, indent=4)


# Delete a database from the history file
def delete_db(filename):
    if not os.path.exists(HISTORY_FILE):
        print(f"Error: History file '{HISTORY_FILE}' does not exist.")
        return

    # Remove the database from the history list
    with open(HISTORY_FILE, "r") as f:
        history_data = json.load(f)

    history_data["databases"] = [
        db for db in history_data["databases"] if db["filename"] != filename
    ]
    with open(HISTORY_FILE, "w") as f:
        json.dump(history_data, f, indent=4)

    # Delete the actual file from the storage directory
    db_file = os.path.join(DATABASE_STORAGE_DIR, filename)
    if os.path.exists(db_file):
        os.remove(db_file)
        typer.echo(f">> Database '{db_file}' deleted successfully.")
    else:
        typer.echo(
            f"Error: File '{db_file}' does not exist or has already been deleted."
        )
