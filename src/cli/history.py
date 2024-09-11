import json
import os
from datetime import datetime
from config import HISTORY_FILE, HISTORY_VERSION


def history_create():
    """Creates a new history file if it doesn't exist."""
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


def get_next_db_filename():
    """Generate the next available database filename based on the date and existing files."""
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


def history_add_db():
    """Adds a new database entry to the history file and marks it as the current one."""
    history_path = os.path.join(os.path.dirname(__file__), HISTORY_FILE)

    if os.path.exists(history_path):
        with open(history_path, "r") as f:
            history_data = json.load(f)
    else:
        history_create()
        with open(history_path, "r") as f:
            history_data = json.load(f)

    new_db_filename = get_next_db_filename()

    history_data["databases"].append(
        {
            "filename": new_db_filename,
            "created_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        }
    )

    history_data["current_db"] = new_db_filename

    with open(history_path, "w") as f:
        json.dump(history_data, f, indent=4)

    print(f"Added new DB to history file: '{new_db_filename}', marked as current DB.")
    return new_db_filename


def get_current_db():
    """Returns the current database filename."""
    history_path = os.path.join(os.path.dirname(__file__), HISTORY_FILE)

    if os.path.exists(history_path):
        with open(history_path, "r") as f:
            history_data = json.load(f)
        return history_data.get("current_db", None)
    else:
        print("History file does not exist.")
        history_create()
        return None
