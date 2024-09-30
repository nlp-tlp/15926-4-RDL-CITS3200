import typer
import requests


def reload_graph():
    try:
        response = requests.get("http://127.0.0.1:5000/ctrl/reload")
        if response.status_code == 200:
            typer.echo("Graph reloaded successfully.")
        else:
            typer.echo(f"Error reloading graph: {response.text}")
    except requests.ConnectionError:
        typer.echo("Server is down, skipping graph reload.")
