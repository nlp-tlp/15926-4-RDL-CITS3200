# Imports
from . import controllers
from flask import jsonify, request, current_app
from rdflib import Graph
from app.blueprints import main, ctrl
from app.config import Config
from app.models import load_selected_db


@main.route("/ping")
def ping():
    """
    Ping route to check if the server is running.

    Returns:
        JSON: A success message with "Pong!"
    """
    return jsonify({"status": "success", "message": "Pong!"}), 200


@main.route("/node/root")
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


@main.route("/search/<string:field>/<path:search_key>", methods=["GET"])
def search(field, search_key):
    """
    Searches the graph by either a node ID (URI) or a label based on the dynamic field in the URL.

    Args:
        field (str): Specifies whether the search is by 'id' (URI) or 'label'.
        search_key (str): The search term, which can be either the URI or label of the node.

    Query Parameters:
        dep (bool): Whether to include deprecated nodes. Default is False.
        limit (int): Maximum number of results to return. Default is 5, max is 25.
        similarity (int): Minimum similarity score of results to return. Default is 75(%)

    Returns:
        JSON: The search results by either node ID (URI) or label.
    """
    # Convert the 'field' to uppercase to make it case-insensitive
    field = field.upper()
    allowed_fields = ["ID", "LABEL"]

    # Extract custom parameters
    include_deprecation = controllers.str_to_bool(
        request.args.get("dep", default=False)
    )
    # Ensure limit is not negative and within max limits
    abs_limit = abs(int(request.args.get("limit", 5)))
    limit = min(abs_limit, int(Config.MAX_SEARCH_LIMIT))

    similarity = abs(int(request.args.get("similarity", 75)))

    try:
        # Check if the graph is available
        if not hasattr(current_app, "graph"):
            raise AttributeError("Graph is not initialised")

        if field not in allowed_fields:
            return jsonify({"error": "Invalid field. Use 'id' or 'label'."}), 400

        results = controllers.search(
            search_key=str(search_key),
            field=field,
            graph=current_app.graph,
            dep=include_deprecation,
            limit=limit,
            min_similarity=similarity,
        )

    except AttributeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal Error"}), 500

    return jsonify({"search_key": search_key, "results": results})


@ctrl.route("/ctrl/reload", methods=["GET"])
def reload_graph():
    """
    Route to reload the RDFLib graph with the currently selected database file.

    Returns:
        JSON: Success message if the graph is reloaded successfully.
    """
    try:
        new_graph = Graph()
        current_app.graph = load_selected_db(graph=new_graph)
        return jsonify({"status": "success", "message": "Graph successfully reloaded."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
