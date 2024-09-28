from server import flaskApp
from app.models import load_latest_db
from rdflib import Graph


def reload_server_graph():
    """
    Reloads the RDFLib graph object stored in the Flask application context.
    """
    try:
        graph = Graph()
        graph = load_latest_db(graph=graph)
        flaskApp.graph = graph
    except Exception as e:
        print(f"Error loading database from history: {e}")
