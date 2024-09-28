#!/usr/bin/env python3

import typer

from history import get_current_db, delete_db, update_current_db, get_all_databases
from database import update_db
from config import HISTORY_VERSION
from serverload import reload_server_graph

app = typer.Typer()  # Initialize Typer app


@app.command()
def main(update: bool = False):
    """
    CLI tool to interact with the database.

    Args:
    - update (bool): To update database straight away.
    """
    # Print MOTD
    motd()

    # If db_update is passed, update the database
    if update:
        typer.echo("Updating the database...")
        update_db()

    else:
        db_name, _ = get_current_db()
        if db_name:
            typer.echo(f"Current database in use: {db_name}")
        else:
            typer.echo("No database found in the history.")

    # Move onto the main menu
    menu()


def motd():
    typer.echo("Welcome to Iso15926Vis CLI for Backend!")
    typer.echo(f"Database history version: '{HISTORY_VERSION}'\n")


def menu():
    while True:
        typer.echo("\n\n\n\n\n\n\n\n\n\n\n\n~~~~~~~~~~~~~~~~ CLI MENU ~~~~~~~~~~~~~~~~")
        typer.echo("Options:")
        typer.echo("Q = Quit the program")
        typer.echo("V = Check the version")
        typer.echo("U = Update the database")
        typer.echo("M = Modify the database in use")

        # Get user input
        choice = input("\nPlease enter your choice (Q/V/U/M): ").strip().upper()
        typer.echo("\n")

        if choice == "Q":
            typer.echo("Exiting the program. Goodbye!")
            break

        elif choice == "V":
            db_name, db_date = get_current_db()
            typer.echo(f"Current database in use: '{db_name}'")
            typer.echo(f"Database was created at '{db_date}'.")

        elif choice == "U":
            typer.echo("Updating the database...")
            update_db()
            typer.echo("Database updated successfully!")

        elif choice == "M":
            typer.echo("Entering Database Version Control menu...")
            modify_db_menu()

        else:
            typer.echo("!! Invalid choice. Please try again.")

        input("Press enter to continue...")


def modify_db_menu():
    dbs = get_all_databases()
    current_db, _ = get_current_db()

    typer.echo(
        "\n\n\n\n\n\n\n\n\n\n\n\n~~~~~~~~~~~~~~~~ Database Version Control (DVC) ~~~~~~~~~~~~~~~~"
    )
    typer.echo(f"Current database in use: {current_db}\n")
    typer.echo("Available databases:")

    # List all available databases
    for i, db in enumerate(dbs, start=1):
        typer.echo(f"{i}. {db['filename']} (Created: {db['created_at']})")

    typer.echo("\nOptions:")
    typer.echo("D = Delete a database")
    typer.echo("C = Change the current database in use")
    typer.echo("Q = Return to previous menu")

    # Get user input for action
    choice = input("\nPlease enter your choice (D/U/Q): ").strip().upper()

    if choice == "D":
        # Delete a database
        delete_choice = int(input("Enter the number of the database to delete: ")) - 1

        # Ensure the current DB cannot be deleted
        if dbs[delete_choice]["filename"] == current_db:
            typer.echo(
                "!! Cannot delete the currently in-use database. Change the database in use first."
            )
        else:
            delete_db(dbs[delete_choice]["filename"])

    elif choice == "C":
        # Update the current database
        update_choice = (
            int(input("Enter the number of the database to set as current: ")) - 1
        )

        new_db = dbs[update_choice]["filename"]
        update_current_db(new_db)
        typer.echo(f">> Database updated to '{new_db}'.")

        reload_server_graph()

    elif choice == "Q":
        # Return to the previous menu
        typer.echo("Returning...")
        return

    else:
        typer.echo("!! Invalid choice. Returning...")


if __name__ == "__main__":
    app()  # Use Typer's app() function to parse CLI arguments
