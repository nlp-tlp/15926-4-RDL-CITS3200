# Imports
import sys
from flask import Flask
from rdflib import Graph
from .models import load_latest_db


def create_app(config):
    # Main application name
    flaskApp = Flask(__name__)

    # Configure flask app
    flaskApp.config.from_object(config)

    # Initialize RDFLib graph
    try:
        graph = Graph()
        graph = load_latest_db(graph=graph)
        flaskApp.graph = graph  # Store the graph in the app context
    except Exception as e:
        print(f"Error loading database from history: {e}")
        sys.exit(1)  # Exist startup if database cant be loaded.

    from app.blueprints import main

    # Register main blueprint
    flaskApp.register_blueprint(main)

    return flaskApp
