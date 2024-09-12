import json

from .config import Config


# Load the latest database (Turtle file) into the RDFLib graph based on the history file.
def load_latest_db(graph):
    try:
        # Load history data
        with open(Config.DB_HISTORY_FILE, "r") as f:
            history_data = json.load(f)

        # Get the latest database filename from history
        latest_db_file = history_data.get("current_db", None)

        if latest_db_file:
            # Load the latest Turtle file into the RDFLib graph
            graph.parse(f"{Config.DB_STORAGE_DIR}/{latest_db_file}", format="turtle")
            return graph
        else:
            raise LookupError("No current database found in history.")

    except Exception as e:
        raise
