import sys
from rdflib import Graph
from app import create_app
from app.config import DeploymentConfig
from app.models import load_selected_db

# Deployment Configuration
flaskApp = create_app(DeploymentConfig)

# Initialize RDFLib graph -- ONLY FOR DEPLOYMENT CONFIGURATION
try:
    graph = Graph()
    graph = load_selected_db(graph=graph)
    flaskApp.graph = graph  # Store within app context
except Exception as e:
    print(f"Error loading database from history: {e}")
    sys.exit(1)
