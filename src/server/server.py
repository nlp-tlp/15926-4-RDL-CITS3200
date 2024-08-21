# Imports
from app import create_app, db
from app.config import TestConfig, DeploymentConfig

# Deployment Configuration
flaskApp = create_app(DeploymentConfig)

# Testing Configuration
# flaskApp = create_app(TestConfig)

# Ensure db is created
with flaskApp.app_context():
    db.create_all()
