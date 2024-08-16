# Imports
from flask import request, redirect, url_for, flash, jsonify
from app.blueprints import main


@main.route("/index")
@main.route("/home")
@main.route("/")
def home() :
  return()