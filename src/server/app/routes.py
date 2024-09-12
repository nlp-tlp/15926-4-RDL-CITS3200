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
    try:
        # Check if the graph is available
        if not hasattr(current_app, "graph"):
            raise AttributeError("Graph is not initialised")

        root_node_info = controllers.get_root_node_info(graph=current_app.graph)

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except AttributeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal Error"}), 500

    if root_node_info:
        return jsonify(root_node_info)

    else:
        return jsonify({"error": "No ROOT found"}), 404


@main.route("/graph/children", methods=["GET"])
def get_children():
    # Extract the custom ID from the query parameters
    node_uri = request.args.get("id")

    # For demonstration, just returning the ID, in practice, you'd fetch children from a graph
    if node_uri:
        try:
            # Check if the graph is available
            if not hasattr(current_app, "graph"):
                raise AttributeError("Graph is not initialised")

            children = controllers.get_children(uri=node_uri, graph=current_app.graph)

        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except AttributeError as e:
            return jsonify({"error": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "Internal Error"}), 500

        return jsonify({"id": node_uri, "children": children})

    else:
        return jsonify({"error": "ID/URI not provided"}), 400


# @main.route("/graph/local-hierarchy/")
