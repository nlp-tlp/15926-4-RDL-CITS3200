# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config):
    # Main application name
    flaskApp = Flask(__name__)

    # Configure flask app
    flaskApp.config.from_object(config)

    # Initialise using flask app
    db.init_app(flaskApp)

    from app.blueprints import main

    flaskApp.register_blueprint(main)

    return flaskApp
