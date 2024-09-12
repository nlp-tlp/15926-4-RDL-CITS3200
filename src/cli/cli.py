import typer

from history import get_current_db
from database import update_db
from config import HISTORY_VERSION

app = typer.Typer()  # Initialize Typer app


@app.command()
def main(update: bool = False, fix: bool = False):
    """
    CLI tool to interact with the database.

    Args:
    - update (bool): To update database straight away.
    - fix (bool): To scan database and fix any errors.
    """
    # Print MOTD
    motd()

    # If db_update is passed, update the database
    if update:
        print("UPDATING DB!")
        update_db()

    else:
        current_db = get_current_db()
        if current_db:
            print(f"Current database in use: {current_db}")
        else:
            print("No database found in the history.")


def motd():
    typer.echo("Welcome to Iso15926Vis CLI for Backend!")
    typer.echo(f"Database history version: '{HISTORY_VERSION}'\n")


if __name__ == "__main__":
    app()  # Use Typer's app() function to parse CLI arguments
