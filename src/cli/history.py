import json
import os
from datetime import datetime

HISTORY_FILE = "history.json"
VERSION_HISTORY_FILE = 1


def history_file_create():
    # Path to the history file
    history_path = os.path.join(os.path.dirname(__file__), HISTORY_FILE)

    # Initialize the history data structure
    history_data = {"version": VERSION_HISTORY_FILE, "databases": [], "current_db": ""}

    # Load existing history if the file exists
    if not os.path.exists(history_path):
        with open(history_path, "w") as f:
            json.dump(history_data, f, indent=4)

    print(f"History file created: '{history_path}'")


def history_file_add_db(new_db_filename):
    # Path to the history file
    history_path = os.path.join(os.path.dirname(__file__), HISTORY_FILE)

    # Initialize the history data structure
    history_data = {"version": VERSION_HISTORY_FILE, "databases": [], "current_db": ""}

    # Load existing history if the file exists
    if os.path.exists(history_path):
        with open(history_path, "r") as f:
            history_data = json.load(f)

    # Update the history with the new database entry
    history_data["version"] = VERSION_HISTORY_FILE
    history_data["databases"].append(
        {
            "filename": new_db_filename,
            "created_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        }
    )

    # Save the updated history back to the file
    with open(history_path, "w") as f:
        json.dump(history_data, f, indent=4)

    print(f"Added new DB to history file: '{new_db_filename}'")
