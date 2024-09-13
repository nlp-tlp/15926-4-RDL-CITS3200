# Imports
import sys
from rdflib import Graph
from app import create_app
from app.config import TestConfig, DeploymentConfig
from app.models import load_latest_db

# Deployment Configuration
flaskApp = create_app(DeploymentConfig)

# Initialize RDFLib graph -- ONLY FOR DEPLOYMENT CONFIGURATION
try:
    graph = Graph()
    graph = load_latest_db(graph=graph)
    flaskApp.graph = graph  # Store the graph in the app context
except Exception as e:
    print(f"Error loading database from history: {e}")
    sys.exit(1)  # Exist startup if database cant be loaded.
