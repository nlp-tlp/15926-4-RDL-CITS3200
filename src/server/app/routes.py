# Imports
# from flask import request, redirect, url_for, flash, jsonify
from flask import redirect
from app.blueprints import main
from app.controllers import update_db


@main.route("/index")
@main.route("/home")
@main.route("/")
def home():
    return "<h1>Welcome to the Home Page!</h1><p>Your Flask application is running successfully.</p>"


@main.route("/update-db")
def db():
    update_db()
    redirect(home)
