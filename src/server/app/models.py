import json
import os

from app.config import Config


def load_latest_db(graph):
    """
    Loads the latest Turtle database file into the RDFLib graph based on the history file.

    Args:
        graph (rdflib.Graph): The RDFLib graph object to load the Turtle data into.

    Raises:
        Exception: If there is an error while loading the database or parsing the Turtle file.

    Returns:
        rdflib.Graph: The RDFLib graph object with the Turtle data loaded, or an empty graph if no database is found.
    """
    try:
        # Check if DB files not yet initialised by CLI
        if (
            os.path.exists(Config.DB_HISTORY_FILE)
            + os.path.exists(Config.DB_STORAGE_DIR)
            != 2
        ):
            print("No current database found in history. Loading an empty graph.")
            return graph

        # DB files found
        with open(Config.DB_HISTORY_FILE, "r") as f:
            history_data = json.load(f)
        latest_db_file = history_data.get("current_db", None)

        if not latest_db_file:
            print("No current database found in history. Loading an empty graph.")
            return graph

        graph.parse(f"{Config.DB_STORAGE_DIR}/{latest_db_file}", format="turtle")
        return graph

    except Exception:
        raise
