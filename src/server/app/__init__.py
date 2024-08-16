# Imports
from flask import Flask

# db = SQLAlchemy()

def create_app(config):
    # Main application name
    flaskApp = Flask(__name__)

    # Configure flask app
    flaskApp.config.from_object(config)
    
    from app.blueprints import main
    flaskApp.register_blueprint(main)
                         
    return flaskApp