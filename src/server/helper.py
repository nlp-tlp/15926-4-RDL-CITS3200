from rdflib import Graph
from server import flaskApp
from app.models import load_latest_db


def reload_graph():
    try:
        new_graph = Graph()
        new_graph = load_latest_db(graph=new_graph)

        # Replace the current graph in the Flask app
        flaskApp.graph = new_graph
        print("Graph successfully reloaded.")
    except Exception as e:
        print(f"Error reloading the graph: {e}")
