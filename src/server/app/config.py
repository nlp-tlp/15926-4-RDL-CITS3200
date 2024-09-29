import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


# Shared configuration
class Config:
    # Root node of graph
    ROOT_NODE_URI = "http://data.15926.org/dm/Thing"

    # Storage location of the database HISTORY file (SHOULD BE RELATIVE)
    DB_HISTORY_FILE = os.path.join(basedir, "../db/history.json")

    # Storage location of the database files (SHOULD BE RELATIVE)
    DB_STORAGE_DIR = os.path.join(basedir, "../db/storage")

    # Maximum possible number of items returned by the search api end points
    MAX_SEARCH_LIMIT = 25


class DeploymentConfig(Config):
    DEBUG = False
    TESTING = False


class TestConfig(Config):
    DEBUG = True
    TESTING = True
