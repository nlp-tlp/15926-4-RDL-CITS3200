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
        order (bool, optional): Whether to order the nodes in alphabetical order. Default is True.

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
    order = controllers.str_to_bool(request.args.get("order", default=True))

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
            order=order,
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


@main.route("/node/parents/<path:node_uri>", methods=["GET"])
def parents(node_uri):
    """
    Fetches the parents of a given node in the graph, including information about their children and other optional details.

    Args:
        node_uri (str): The URI of the node to fetch parents for.

    Query Parameters:
        dep (bool, optional): Whether to include deprecated nodes. Default is False.
        extra_children (bool, optional): Whether to include extra children of the parents, excluding the current node. Default is True.
        children_ex_parents (bool, optional): Whether to include extra parents for each child in the parent's children. Default is False.
        has_parent (bool, optional): Whether to include a boolean flag indicating if the parent nodes have other parents. Default is True.
        order (bool, optional): Whether to order the parents alphabetically. Default is True.

    Raises:
        ValueError: If the node does not exist in the graph.
        AttributeError: If the graph is not initialized in the application context.
        Exception: For any other internal error.

    Returns:
        JSON: A JSON object with the expanded node id and the hierarchy.
    """
    # Extract the custom parameters
    include_deprecation = controllers.str_to_bool(
        request.args.get("dep", default=False)
    )
    include_extra_children = controllers.str_to_bool(
        request.args.get("extra_children", default=True)
    )
    include_parents_children_extra_parents = controllers.str_to_bool(
        request.args.get("children_ex_parents", default=False)
    )
    include_has_parent = controllers.str_to_bool(
        request.args.get("has_parent", default=True)
    )
    order = controllers.str_to_bool(request.args.get("order", default=True))

    try:
        # Check if the graph is available
        if not hasattr(current_app, "graph"):
            raise AttributeError("Graph is not initialised")

        hierarchy = controllers.get_parents(
            uri=node_uri,
            graph=current_app.graph,
            dep=include_deprecation,
            include_ex_children=include_extra_children,
            children_ex_parents=include_parents_children_extra_parents,
            parent_flag=include_has_parent,
            order=order,
        )

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except AttributeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal Error"}), 500

    return jsonify({"id": node_uri, "parents": hierarchy})


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
    
    
@main.route("/node/selected-info/<path:node_uri>", methods=["GET"])
def selected_info(node_uri):
    """
    Retrieves selected information about a given node in the RDFLib graph,
    including its label, deprecation date, and whether it has children or parents.

    Args:
        node_uri (str): The URI of the node to retrieve information for.

    Raises:
        ValueError: If the node does not exist in the graph.
        AttributeError: If the graph is not initialized.

    Returns:
        JSON: The selected information for the given node.
    """
    try:
        # Check if the graph is available
        if not hasattr(current_app, "graph"):
            raise AttributeError("Graph is not initialised")

        # Fetch the node information
        node_info = controllers.get_node_info_with_relations(uri=node_uri, graph=current_app.graph)

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except AttributeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal Error"}), 500

    return jsonify(node_info)


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

    try:
        # Check if the graph is available
        if not hasattr(current_app, "graph"):
            raise AttributeError("Graph is not initialised")

        if field not in allowed_fields:
            return jsonify({"error": "Invalid field. Use 'id' or 'label'."}), 400

        results = controllers.search(
            search_key=search_key,
            field=field,
            graph=current_app.graph,
            dep=include_deprecation,
            limit=limit,
        )

    except AttributeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal Error"}), 500

    return jsonify({"search_key": search_key, "results": results})


@main.route("/graph/local-hierarchy/<path:node_uri>", methods=["GET"])
def local_hierarchy(node_uri):
    """
    Fetches the local hierarchy for a given node in the RDF graph, including its parents, children, and other optional details.

    Args:
        node_uri (str): The URI of the node to fetch the local hierarchy for.

    Query Parameters:
        dep (bool, optional): Whether to include deprecated nodes. Default is False.
        extra_parents (bool, optional): Whether to include extra parents for each node. Default is True.
        has_children (bool, optional): Whether to include a boolean flag indicating if each node has children. Default is True.
        has_parent (bool, optional): Whether to include a boolean flag indicating if each node has parents. Default is True.
        order (bool, optional): Whether to order the nodes alphabetically by label. Default is True.
        incl_children (bool, optional): Whether to include the direct children of the selected node. Default is True.

    Raises:
        ValueError: If the node does not exist in the graph.
        AttributeError: If the graph is not initialized in the application context.
        Exception: For any other internal error.

    Returns:
        JSON: A JSON object containing the id of the centre node and the hierarchy (level above and below):
    """
    # Extract custom parameters
    include_deprecation = controllers.str_to_bool(
        request.args.get("dep", default=False)
    )
    include_extra_parents = controllers.str_to_bool(
        request.args.get("extra_parents", default=True)
    )
    include_has_children = controllers.str_to_bool(
        request.args.get("has_children", default=True)
    )
    include_has_parent = controllers.str_to_bool(
        request.args.get("has_parent", default=False)
    )
    include_direct_children = controllers.str_to_bool(
        request.args.get("incl_children", default=True)
    )
    order = controllers.str_to_bool(request.args.get("order", default=True))

    try:
        # Check if the graph is available
        if not hasattr(current_app, "graph"):
            raise AttributeError("Graph is not initialized")

        # Fetch the local hierarchy
        hierarchy = controllers.get_local_hierarchy_to_root(
            uri=node_uri,
            graph=current_app.graph,
            dep=include_deprecation,
            ex_parents=include_extra_parents,
            children_flag=include_has_children,
            parent_flag=include_has_parent,
            order=order,
            include_children=include_direct_children,
        )

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except AttributeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal Error"}), 500

    return jsonify({"centre_id": node_uri, "hierarchy": hierarchy})
