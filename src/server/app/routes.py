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


@main.route("/node/children/<path:node_uri>", methods=["GET"])
def children(node_uri):
    """
    Fetches the children of a given node in the graph.

    Args:
        node_uri (str): The URI of the node to fetch children for.

    Query Parameters:
        dep (bool): Whether to include deprecated nodes. Default is False.
        extra_parents (bool): Whether to include extra parents for each child. Default is True.
        has_children (bool): Whether to include a boolean flag indicating if the child has children. Default is True.

    Raises:
        ValueError: If the node does not exist in the graph.
        AttributeError: If the graph is not initialized.
        Exception: For any other internal error.

    Returns:
        JSON: The id of the node, the children of the given node in alphabetical order, along with other requested details.
    """
    # Extract the custom parameters
    include_deprecation = controllers.str_to_bool(
        request.args.get("dep", default=False)
    )
    include_extra_parents = controllers.str_to_bool(
        request.args.get("extra_parents", default=True)
    )
    include_has_children = controllers.str_to_bool(
        request.args.get("has_children", default=True)
    )
    levels = request.args.get("levels", default=1, type=int)

    try:
        # Check if the graph is available
        if not hasattr(current_app, "graph"):
            raise AttributeError("Graph is not initialised")

        children = controllers.get_children(
            uri=node_uri,
            graph=current_app.graph,
            dep=include_deprecation,
            ex_parents=include_extra_parents,
            children_flag=include_has_children,
            order=True,
            levels=levels,
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


@main.route("/node/local-hierarchy/<path:node_uri>", methods=["GET"])
def local_hierarchy(node_uri):
    # Extract the required parameters
    dist_above = request.args.get("above", default=6, type=int)
    dist_below = request.args.get("below", default=6, type=int)

    if not node_uri:
        return jsonify({"error": "ID/URI not provided"}), 400

    try:
        # Check if the graph is available
        if not hasattr(current_app, "graph"):
            raise AttributeError("Graph is not initialized")

        # Fetch the local hierarchy
        hierarchy = controllers.get_local_hierarchy(
            uri=node_uri,
            graph=current_app.graph,
            dist_below=dist_below,
            dist_above=dist_above,
        )

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except AttributeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal Error"}), 500

    return jsonify({"id": node_uri, "hierarchy": hierarchy})
