# Imports
from . import controllers
from flask import jsonify, request, current_app
from app.blueprints import main
from app.config import Config


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


@main.route("/node/children/<path:node_uri>", methods=["GET"])
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
            order=True,
        )

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except AttributeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal Error"}), 500

    return jsonify({"id": node_uri, "children": children})


@main.route("/node/children/", methods=["GET"])
@main.route("/node/children", methods=["GET"])
def invalid_children():
    """
    Fallback route for invalid children requests.

    Returns:
        JSON: Error message indicating the ID/URI was not provided.
    """
    return (
        jsonify({"error": "ID/URI not provided. Must use '/node/children/<id>'"}),
        400,
    )


@main.route("/node/info/<path:node_uri>", methods=["GET"])
def info(node_uri):
    """
    Retrieves detailed information about a given node in the RDFLib graph,
    including various properties such as label, types, deprecation dates,
    and additional properties if specified.

    Args:
        node_uri (str): The URI of the node to retrieve information for.

    Query Parameters:
        all_info (bool): A query parameter that specifies whether to retrieve all
                         available node information (default: True).

    Returns:
        JSON: The information for the given node.
    """
    # Extract extra parameters
    include_all_info = controllers.str_to_bool(
        request.args.get("all_info", default=True)
    )

    try:
        # Check if the graph is available
        if not hasattr(current_app, "graph"):
            raise AttributeError("Graph is not initialised")

        info = controllers.get_all_node_info(
            uri=node_uri, graph=current_app.graph, all_info=include_all_info
        )

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except AttributeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal Error"}), 500

    return jsonify(info)


@main.route("/node/info/", methods=["GET"])
@main.route("/node/info", methods=["GET"])
def invalid_info():
    """
    Handles requests to '/node/info' where no node URI is provided.
    Returns an error message with status code 400.

    Returns:
        JSON: Error message indicating the ID/URI was not provided.
    """
    return (
        jsonify({"error": "ID/URI not provided. Must use '/node/info/<id>'"}),
        400,
    )


@main.route("/search/id/<path:node_uri>", methods=["GET"])
def search_by_id(node_uri):
    """
    Searches the graph by a node ID (URI) and returns matching nodes.

    Args:
        node_uri (str): The URI of the node to search for.

    Query Parameters:
        dep (bool): Whether to include deprecated nodes. Default is False.
        limit (int): Maximum number of results to return. Default is 5, max is 25.

    Returns:
        JSON: The search results by node ID.
    """
    # Extract custom parameters
    include_deprecation = controllers.str_to_bool(
        request.args.get("dep", default=False)
    )
    limit = min(int(request.args.get("limit", 5)), int(Config.MAX_SEARCH_LIMIT))

    try:
        # Check if the graph is available
        if not hasattr(current_app, "graph"):
            raise AttributeError("Graph is not initialised")

        results = controllers.search(
            search_key=node_uri,
            field="URI",
            graph=current_app.graph,
            dep=include_deprecation,
            limit=limit,
        )

    except AttributeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal Error"}), 500

    return jsonify({"search_key": node_uri, "results": results})


@main.route("/search/label/<path:node_label>", methods=["GET"])
def search_by_label(node_label):
    """
    Searches the graph by a node label and returns matching nodes.

    Args:
        node_uri (str): The label of the node to search for.

    Query Parameters:
        dep (bool): Whether to include deprecated nodes. Default is False.
        limit (int): Maximum number of results to return. Default is 5, max is 25.

    Returns:
        JSON: The search results by node label.
    """
    # Extract custom parameters
    include_deprecation = controllers.str_to_bool(
        request.args.get("dep", default=False)
    )
    limit = min(int(request.args.get("limit", 5)), int(Config.MAX_SEARCH_LIMIT))

    try:
        # Check if the graph is available
        if not hasattr(current_app, "graph"):
            raise AttributeError("Graph is not initialised")

        results = controllers.search(
            search_key=node_label,
            field="LABEL",
            graph=current_app.graph,
            dep=include_deprecation,
            limit=limit,
        )

    except AttributeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal Error"}), 500

    return jsonify({"search_key": node_label, "results": results})
