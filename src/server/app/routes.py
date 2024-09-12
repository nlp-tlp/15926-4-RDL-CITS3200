# Imports
from . import controllers
from flask import jsonify, request, current_app
from app.blueprints import main


@main.route("/index")
@main.route("/home")
@main.route("/")
def home():
    return "<h1>Welcome to the Home Page!</h1><p>Your Flask application is running successfully.</p>"


@main.route("/ping")
def ping():
    return jsonify({"status": "success", "message": "Pong!"}), 200


@main.route("/graph/root")
def root():
    root_node = controllers.get_root_node()


@main.route("/graph/children", methods=["GET"])
def get_children():
    # Extract the custom ID from the query parameters
    node_uri = request.args.get("id")

    # For demonstration, just returning the ID, in practice, you'd fetch children from a graph
    if node_uri:
        children = controllers.get_children(uri=node_uri, graph=current_app.graph)
        return jsonify({"id": node_uri, "children": children})
    else:
        return jsonify({"error": "ID/URI not provided"}), 400


# @main.route("/graph/local-hierarchy/")
