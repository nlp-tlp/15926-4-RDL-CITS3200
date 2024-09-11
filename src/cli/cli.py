import typer
import time
import http.client

from history import history_file_create
from db3v2 import update_db

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

    # if not check_db():
    #     exit(1)

    # history_file_create()

    print("UPDATING DB!")
    update_db()


def motd():
    typer.echo("Welcome to Iso15926Vis CLI for Backend!")
    typer.echo(f"Database is at version '{DB_VERSION}'.")


def check_db(host="localhost", port=8890, timeout=3):
    conn = http.client.HTTPConnection(host, port)
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            conn.request("GET", "/sparql")
            response = conn.getresponse()
            if response.status == 200:
                print("Database server (Virtuoso) is up and running.")
                return True
        except (http.client.HTTPException, ConnectionRefusedError):
            pass
        time.sleep(5)

    print(
        "Timeout: Database server (Virtuoso) is not running. Please start it before continuing."
    )
    return False


if __name__ == "__main__":
    main()
