# Imports
# from flask import request, redirect, url_for, flash, jsonify
from flask import jsonify
from app.blueprints import main


@main.route("/index")
@main.route("/home")
@main.route("/")
def home():
    return "<h1>Welcome to the Home Page!</h1><p>Your Flask application is running successfully.</p>"


@main.route("/ping")
def ping():
    return jsonify({"status": "success", "message": "Pong!"}), 200
