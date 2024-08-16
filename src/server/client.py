# Imports
from app import create_app
from app.config import TestConfig, DeploymentConfig

# Deployment Configuration
flaskApp = create_app(DeploymentConfig)

# Testing Configuration
# flaskApp = create_app(TestConfig)
