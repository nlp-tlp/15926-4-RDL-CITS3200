import typer
import os
import json
from datetime import datetime

from history import history_file_create
from db import update_db

# Global variables
DB_VERSION = "24/8/24"
VERSION_HISTORY_FILE = 1
HISTORY_FILE = "history.json"


def main(db_update: bool = False, fix: bool = False):
    """
    CLI tool to interact with the database.

    Args:
    - db_update (bool): To update database straight away.
    - fix (bool): To scan database and fix any errors.
    """
    # Print MOTD
    motd()

    history_file_create()

    print("UPDATING DB!")
    update_db()


def motd():
    typer.echo("Welcome to Iso15926Vis CLI for Backend!")
    typer.echo(f"Database is at version '{DB_VERSION}'.")


if __name__ == "__main__":
    main()
