# Imports
from . import controllers
from flask import jsonify, request, current_app
from app.blueprints import main


@main.route("/ping")
def ping():
    """
    Ping route to check if the server is running.

    Returns:
        JSON: A success message with "Pong!"
    """
    return jsonify({"status": "success", "message": "Pong!"}), 200


@main.route("/graph/root")
def root():
    """
    Route to fetch the root node information from the graph.

    Raises:
        ValueError: If the root node does not exist.
        AttributeError: If the graph is not initialized.

    Returns:
        JSON: Information about the root node.
    """
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


@main.route("/graph/children/<path:node_uri>", methods=["GET"])
def children(node_uri):
    """
    Fetches the children of a given node in the graph.

    Args:
        node_uri (str): The URI of the node to fetch children for.

    Query Parameters:
        dep (bool): Whether to include deprecated nodes. Default is False.
        extra_parents (bool): Whether to include extra parents for each child. Default is True.

    Raises:
        ValueError: If the node does not exist in the graph.
        AttributeError: If the graph is not initialized.
        Exception: For any other internal error.

    Returns:
        JSON: The children of the given node, along with other requested details.
    """
    # Extract the custom parameters
    include_deprecation = controllers.str_to_bool(
        request.args.get("dep", default=False)
    )
    include_extra_parents = controllers.str_to_bool(
        request.args.get("extra_parents", default=True)
    )

    try:
        # Check if the graph is available
        if not hasattr(current_app, "graph"):
            raise AttributeError("Graph is not initialised")

        children = controllers.get_children(
            uri=node_uri,
            graph=current_app.graph,
            dep=include_deprecation,
            ex_parents=include_extra_parents,
        )

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except AttributeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal Error"}), 500

    return jsonify({"id": node_uri, "children": children})


@main.route("/graph/children/", methods=["GET"])
@main.route("/graph/children", methods=["GET"])
def invalid_children():
    """
    Fallback route for invalid children requests.

    Returns:
        JSON: Error message indicating the ID/URI was not provided.
    """
    return (
        jsonify({"error": "ID/URI not provided. Must use '/graph/children/<id>'"}),
        400,
    )
