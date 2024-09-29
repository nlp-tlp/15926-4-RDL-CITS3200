from flask import Flask
from flask_cors import CORS


def create_app(config):
    """
    Creates and configures a Flask application instance.

    Args:
        config (object): The configuration object used to configure the Flask app.

    Returns:
        flask.Flask: A configured Flask application instance.

    Registers:
        - The 'main' blueprint from the 'app.blueprints.main' module.
    """
    # Main application name
    flaskApp = Flask(__name__)

    # Configure flask app
    flaskApp.config.from_object(config)

    # Enable CORS
    CORS(flaskApp)

    from app.blueprints import main

    # Register main blueprint
    flaskApp.register_blueprint(main)

    return flaskApp
