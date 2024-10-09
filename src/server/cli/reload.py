import typer
import requests
from cli.config import SERVER_PORT


def reload_graph():
    try:
        response = requests.get(f"http://127.0.0.1:{SERVER_PORT}/ctrl/reload")
        if response.status_code == 200:
            typer.echo("Graph reloaded successfully.")
        else:
            typer.echo(f"Error reloading graph: {response.text}")
    except requests.ConnectionError:
        typer.echo("Server is down, skipping graph reload.")
