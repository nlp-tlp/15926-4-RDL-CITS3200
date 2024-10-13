import json
import os

from app.config import Config

loaded_db_file = None


def load_selected_db(graph):
    """
    Loads the selected Turtle database file into the RDFLib graph based on the history file.

    Args:
        graph (rdflib.Graph): The RDFLib graph object to load the Turtle data into.

    Raises:
        Exception: If there is an error while loading the database or parsing the Turtle file.

    Returns:
        rdflib.Graph: The RDFLib graph object with the Turtle data loaded, or an empty graph if no database is found.
    """
    global loaded_db_file
    try:
        # Check if DB files not yet initialised by CLI
        if (
            os.path.exists(Config.DB_HISTORY_FILE)
            + os.path.exists(Config.DB_STORAGE_DIR)
            != 2
        ):
            print_error(
                "ERROR: No current database found in history! Loading an empty graph.\nPlease run the CLI tool and update the database: `python3 cli.py`."
            )
            return graph

        # DB files found
        with open(Config.DB_HISTORY_FILE, "r") as f:
            history_data = json.load(f)
        current_db_file = history_data.get("current_db", None)

        if not current_db_file:
            print_error(
                "ERROR: No current database found in history! Loading an empty graph.\nPlease run the CLI tool and update the database: `python3 cli.py`."
            )
            return graph
        if loaded_db_file == current_db_file:
            print("Warning: Selected database file already loaded, aborting reload.")
            return graph

        graph.parse(f"{Config.DB_STORAGE_DIR}/{current_db_file}", format="turtle")
        loaded_db_file = current_db_file

        return graph

    except Exception:
        raise


def print_error(msg):
    """
    Prints a error message with header and footer to make it more distinguishable.
    """
    print(
        "\n\n\n-----------------------------------------------------------------------------\n"
    )
    print(msg)
    print(
        "\n-----------------------------------------------------------------------------\n\n"
    )
