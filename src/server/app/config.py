import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


# Shared configuration
class Config:
    ROOT_NODE_URI = "http://data.15926.org/dm/Thing"  # Root node of graph
    DB_HISTORY_FILE = os.path.join(basedir, "../../db/history.json")
    DB_STORAGE_DIR = os.path.join(basedir, "../../db/storage")
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "default-key-for-testing")
    # Set local secret key with
    # BASH: echo 'export FLASK_SECRET_KEY="your_secret_key_here"' >> ~/.bashrc && source ~/.bashrc
    # WINDOWS CMD: set FLASK_SECRET_KEY=your_secret_key_here
    # with dotenv, you can instead create a .env file and set a local secret key in the same style as Windows


class DeploymentConfig(Config):
    DEBUG = False
    TESTING = False


class TestConfig(Config):
    DEBUG = True
    TESTING = True
