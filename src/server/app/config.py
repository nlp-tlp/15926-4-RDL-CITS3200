import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


# Shared configuration
class Config:
    ROOT_NODE_URI = "http://data.15926.org/dm/Thing"  # Root node of graph
    DB_HISTORY_FILE = os.path.join(
        basedir, "../../db/history.json"
    )  # Storage location of the database HISTORY file (SHOULD BE RELATIVE)
    DB_STORAGE_DIR = os.path.join(
        basedir, "../../db/storage"
    )  # Storage location of the database files (SHOULD BE RELATIVE)
    MAX_SEARCH_LIMIT = (
        25  # Maximum possible number of items returned by the search api end points
    )


class DeploymentConfig(Config):
    DEBUG = False
    TESTING = False


class TestConfig(Config):
    DEBUG = True
    TESTING = True
