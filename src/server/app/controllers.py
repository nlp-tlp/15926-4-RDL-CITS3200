from app.config import Config
from rdflib import URIRef, Literal, RDF, RDFS, Namespace

# Define the namespace for meta and SKOS
META = Namespace("http://data.15926.org/meta/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")


def get_root_node() -> str:
    """
    Retrieves the root node URI from the configuration.

    Returns:
        str: The URI of the root node from the configuration.
    """
    return Config.ROOT_NODE_URI


def check_uri_exists(uri: str, graph) -> bool:
    """
    Checks if a given URI exists as a subject in the RDFLib graph.

    Args:
        uri (str): The URI to check.
        graph (rdflib.Graph): The RDFLib graph to query.

    Returns:
        bool: True if the URI exists in the graph, otherwise False.
    """
    uri_ref = URIRef(uri)  # Convert the URI string to an RDFLib URIRef object

    # True if exist any tripple with URI as the subject
    return any(graph.triples((uri_ref, None, None)))


# Get only the node's LABEL and DEPRECATION DATE
def get_basic_node_info(uri: str, graph, default_dep: bool = False) -> dict[str, any]:
    """
    Retrieves basic information about a node, including its label and deprecation date.

    Args:
        uri (str): The URI of the node to fetch information for.
        graph (rdflib.Graph): The RDFLib graph to query.
        default_dep (bool, optional): Whether to include 'dep' in the dictionary by default. (Default is False).

    Returns:
        dict: A dictionary containing the node's 'id', 'label', and 'dep' (deprecation date, if any).
    """
    # Default structure setup
    if default_dep:
        node_info = {"id": str(uri), "label": None, "dep": None}
    else:
        node_info = {"id": str(uri), "label": None}

    uri_ref = URIRef(uri)  # Ensure uri is a ref before querying

    # Query for the label of the node
    for _, _, label in graph.triples((uri_ref, RDFS.label, None)):
        if isinstance(label, Literal):
            node_info["label"] = str(label)

    # Query for the deprecation date
    for _, _, deprecation_date in graph.triples(
        (uri_ref, META.valDeprecationDate, None)
    ):
        if isinstance(deprecation_date, Literal):
            node_info["dep"] = str(deprecation_date)

    return node_info

def get_node_info_with_relations(uri: str, graph) -> dict[str, any]:
    """
    Retrieves information about a node, including its label, deprecation date, and whether it has children or parents.

    Args:
        uri (str): The URI of the node to fetch information for.
        graph (rdflib.Graph): The RDFLib graph to query.

    Returns:
        dict: A dictionary containing the node's 'id', 'label', 'dep', 'has_children', and 'has_parents'.
    """
    node_info = {"id": str(uri), "label": None, "dep": None, "has_children": False, "has_parents": False}

    uri_ref = URIRef(uri)  # Ensure uri is a ref before querying

    # Query for the label of the node
    for _, _, label in graph.triples((uri_ref, RDFS.label, None)):
        if isinstance(label, Literal):
            node_info["label"] = str(label)

    # Query for the deprecation date
    for _, _, deprecation_date in graph.triples((uri_ref, META.valDeprecationDate, None)):
        if isinstance(deprecation_date, Literal):
            node_info["dep"] = str(deprecation_date)

    # Check if the node has children
    node_info["has_children"] = has_children(uri, graph, dep=False)

    # Check if the node has parents
    node_info["has_parents"] = has_parents(uri, graph, dep=False)

    return node_info

# Get all information (predicates and objects) for a given node in the RDFLib graph.
def get_all_node_info(
    uri: str, graph, all_info: bool = True, default_dep: bool = True
) -> dict[str, any]:
    """
    Retrieves all available information about a given node in the RDFLib graph. This includes
    specific properties such as label, types, deprecation date, definition, and parent nodes
    (subClassOf). If 'all_info' is set to True, additional properties are also returned.

    Args:
        uri (str): The URI of the node to retrieve information for.
        graph (rdflib.Graph): The RDFLib graph to query the node's information from.
        all_info (bool, optional): A flag indicating whether to retrieve additional properties (default: True).
        default_dep (bool, optional): Whether to include 'dep' in the dictionary by default. (Default is True).

    Returns:
        dict: A dictionary containing all available information about the node, including:
            - id (str): The URI of the node.
            - label (str, optional): The rdfs:label value of the node.
            - types (list of str): A list of rdf:type values (if the node has multiple types).
            - dep (str, optional): The meta:valDeprecationDate value (deprecation date).
            - definition (str, optional): The skos:definition of the node.
            - parents (list of str): A list of URIs for parent nodes (rdfs:subClassOf).
            - properties (dict): A dictionary of other predicates and their corresponding objects (only included if 'all_info' is True).

    Raises:
        ValueError: If the provided URI does not exist within the RDFLib graph.
    """
    # Initialise dictionary based on option to include all extra properties.
    node_info = {
        "id": str(uri),
        "label": None,  # Handle rdfs:label
        "types": [],  # Handle multiple rdf:type entries
        "definition": None,  # Handle skos:definition
        "parents": [],  # Handle rdfs:subClassOf
    }

    if all_info:
        node_info["properties"] = {}  # Handle anything else

    if default_dep:
        node_info["dep"] = None  # Handle meta/valDeprecationDate

    # Ensure node exists within the database
    if not check_uri_exists(uri=uri, graph=graph):
        raise ValueError(f"URI '{uri}' does not exist within the database")

    uri_ref = URIRef(uri)

    # Query for all triples where the node is the subject
    for predicate, obj in graph.predicate_objects(subject=uri_ref):
        # If the predicate is rdfs:label, store it separately
        if predicate == RDFS.label and isinstance(obj, Literal):
            node_info["label"] = str(obj)

        # If the predicate is rdf:type, store it in the 'types' list
        elif predicate == RDF.type:
            node_info["types"].append(str(obj))

        # If the predicate is the deprecation date, store it separately
        elif predicate == META.valDeprecationDate and isinstance(obj, Literal):
            node_info["dep"] = str(obj)

        # If the predicate is skos:definition, store it separately
        elif predicate == SKOS.definition and isinstance(obj, Literal):
            node_info["definition"] = str(obj)

        # If the predicate is rdfs:subClassOf, store it in the 'parents' list
        elif predicate == RDFS.subClassOf:
            node_info["parents"].append(str(obj))

        else:
            if all_info:
                # Add the predicate and object to the 'properties' dictionary
                pred_str = str(predicate)
                obj_str = str(obj)

                # Store multiple values under the same predicate
                if pred_str in node_info["properties"]:
                    node_info["properties"][pred_str].append(obj_str)
                else:
                    node_info["properties"][pred_str] = [obj_str]

    return node_info


def get_root_node_info(graph) -> dict[str, any]:
    """
    Retrieves information about the root node of the graph.

    Args:
        graph (rdflib.Graph): The RDFLib graph to query.

    Raises:
        ValueError: If the root node does not exist in the graph.

    Returns:
        dict: A dictionary containing the root node's 'id', 'label', and 'dep' (deprecation date, if any).
    """
    root_node_uri = get_root_node()  # Retrieve root node URI from config
    root_node_ref = URIRef(root_node_uri)  # Convert to URIRef for querying

    if not check_uri_exists(uri=root_node_uri, graph=graph):
        raise ValueError(f"URI '{root_node_uri}' does not exist within the database")

    # Use the helper function to get root node info
    return get_basic_node_info(root_node_ref, graph)


def has_children(uri: str, graph, dep: bool) -> bool:
    """
    Checks if a given node has any children, considering the deprecation status.

    Args:
        uri (str): The URI of the node to check for children.
        graph (rdflib.Graph): The RDFLib graph to query.
        dep (bool): Whether to include deprecated nodes.

    Returns:
        bool: True if the node has children, otherwise False.
    """
    uri_ref = URIRef(uri)  # Convert the URI string to an RDFLib URIRef object

    # Query the graph for triples where the given URI is the object of rdfs:subClassOf (i.e., if any triples are found, the node has children)
    for child, _, _ in graph.triples((None, RDFS.subClassOf, uri_ref)):
        # Check deprecation flag
        if dep:
            return True
        else:
            # Directly query for the deprecation date of the child node
            deprecated = any(graph.triples((child, META.valDeprecationDate, None)))
            if not deprecated:
                return True

    return False


def has_parents(uri: str, graph, dep: bool) -> bool:
    """
    Checks if a given node has any parents, considering the deprecation status.

    Args:
        uri (str): The URI of the node to check for parents.
        graph (rdflib.Graph): The RDFLib graph to query.
        dep (bool): Whether to include deprecated nodes.

    Returns:
        bool: True if the node has parents, otherwise False.
    """
    uri_ref = URIRef(uri)  # Convert the URI string to an RDFLib URIRef object

    # Query the graph for triples where the given URI is the subject of rdfs:subClassOf (i.e., if any triples are found, the node has parents)
    for _, _, parent in graph.triples((uri_ref, RDFS.subClassOf, None)):
        # Check deprecation flag
        if dep:
            return True
        else:
            # Directly query for the deprecation date of the parent node
            deprecated = any(graph.triples((parent, META.valDeprecationDate, None)))
            if not deprecated:
                return True

    return False


def get_children(
    uri: str,
    graph,
    dep: bool = False,
    ex_parents: bool = True,
    children_flag: bool = True,
    order: bool = True,
    ignore_id: str = None,
    inclusion_list: list = None,
) -> list[dict[str, any]]:
    """
    Retrieves the children of a given node, with optional inclusion of deprecated nodes and extra parents.

    Args:
        uri (str): The URI of the node to fetch children for.
        graph (rdflib.Graph): The RDFLib graph to query.
        dep (bool, optional): Whether to include deprecated nodes. (default: False).
        ex_parents (bool, optional): Whether to include extra parents for each child. (default: True).
        children_flag (bool, optional): Whether to include a boolean flag indicating if the child has children. (default: True).
        order (bool, optional): A flag indicating whether to order the children alphabetically (default: True).
        ignore_id (str, optional): The URI to exclude from the results (default: None).
        inclusion_list (list, optional): A list of URIs to include in the results (default: None).

    Raises:
        ValueError: If the node does not exist in the graph.

    Returns:
        list: A list of dictionaries, each containing information about a child node.
    """
    children_set = set()  # Keep only unique children
    children_list = []
    uri_ref = URIRef(uri)  # Convert the URI string to an RDFLib URIRef object

    if not check_uri_exists(uri=uri, graph=graph):
        raise ValueError(f"URI '{uri}' does not exist within the database")

    # Query the graph for triples where the given URI is an object of rdfs:subClassOf
    for child, _, parent in graph.triples((None, RDFS.subClassOf, uri_ref)):
        # If the node is being ignored, skip it (including a node being a child of itself)
        if (str(child) == uri) or (ignore_id and str(child) == ignore_id):
            continue

        # Include only if part of the inclusion_list (if specified)
        if (inclusion_list) and (str(child) not in inclusion_list):
            continue

        if child not in children_set:
            # Use the helper function to get child info
            child_info = get_basic_node_info(child, graph)

            # If ignoring deprecated nodes and a node has a deprecation date, then skip it
            if not dep and child_info.get("dep"):
                continue

            # Add the child to the set and the list
            children_set.add(child)

            # If ex_parents is True, find any additional parents
            if ex_parents:
                extra_parents_list = []  # Initialise an empty list for extra parents

                for _, _, other_parent in graph.triples((child, RDFS.subClassOf, None)):
                    if str(other_parent) != str(parent):
                        # Get info for the extra parent and add it to the extra_parents list
                        extra_parent_info = {"id": str(other_parent)}
                        extra_parents_list.append(extra_parent_info)

                # Only add the 'extra_parents' field if there are extra parents
                if extra_parents_list:
                    child_info["extra_parents"] = extra_parents_list

            # Add the 'has_children' field
            if children_flag:
                child_info["has_children"] = has_children(str(child), graph, dep)

            # Append the child info to the children list
            children_list.append(child_info)

    # Order the children by their label if 'order' is set to True
    if order:
        children_list.sort(key=lambda x: (x.get("label") or ""))

    return children_list


def search(search_key, field, graph, dep=False, limit=5):
    """
    Search the RDFLib graph for nodes by URI or label, with optional filtering for deprecated nodes.

    Args:
        search_key (str): The search term (either part of a URI or part of a label).
        field (str): The field to search by ('URI' or 'LABEL').
        graph (rdflib.Graph): The RDFLib graph to query.
        dep (bool, optional): Whether to include deprecated nodes. Defaults to False.
        limit (int, optional): Maximum number of results to return. Defaults to 5.

    Returns:
        list: A list of unique dictionaries containing node information.
    """

    results = []
    unique_subjects = set()  # Set to track unique subjects
    search_key_lower = search_key.lower()
    count = 0

    # Check if the field is "LABEL"
    if field.upper() == "LABEL":
        # Search by label (rdfs:label) for partial match
        for subject, _, obj in graph.triples((None, RDFS.label, None)):
            if isinstance(obj, Literal) and search_key_lower in str(obj).lower():
                if subject in unique_subjects:
                    continue  # Skip if subject is already added

                # Get basic node info
                node_info = get_basic_node_info(subject, graph)

                # Skip if we don't want deprecated nodes
                if not dep and node_info.get("dep"):
                    continue

                results.append(node_info)
                unique_subjects.add(subject)  # Track this subject
                count += 1

                if count >= limit:
                    break

    # Otherwise default to "URI"
    else:
        # Default or explicit "URI" search (substring match)
        for subject in graph.subjects():
            if search_key_lower in str(subject).lower():
                if subject in unique_subjects:
                    continue  # Skip if subject is already added

                node_info = get_basic_node_info(subject, graph)

                # Skip if we don't want deprecated nodes
                if not dep and node_info.get("dep"):
                    continue

                results.append(node_info)
                unique_subjects.add(subject)  # Track this subject
                count += 1

                if count >= limit:
                    break

    return results


def get_parents(
    uri: str,
    graph,
    dep: bool = False,
    include_ex_children: bool = False,
    children_ex_parents: bool = False,
    parent_flag: bool = True,
    order: bool = True,
) -> list[dict[str, any]]:
    """
    Retrieves the parents of a given node and ensures that its children are unique across all parents.

    Args:
        uri (str): The URI of the node to fetch parents for.
        graph (rdflib.Graph): The RDFLib graph to query.
        dep (bool, optional): Whether to include deprecated nodes. (default: False).
        include_ex_children(bool, optional): Whether to include children other then uri in `ex_children` field (default: False).
        children_ex_parents (bool, optional): Whether to include extra parents for each child in parent's children. (default: True).
        order (bool, optional): A flag indicating whether to order the parents alphabetically by their label (default: True).

    Raises:
        ValueError: If the node does not exist in the graph.

    Returns:
        list: A list of dictionaries, each containing information about a parent node.
    """
    hierarchy = []
    uri_ref = URIRef(uri)  # Convert the URI string to an RDFLib URIRef object
    num_parents = 0

    if not check_uri_exists(uri=uri, graph=graph):
        raise ValueError(f"URI '{uri}' does not exist within the database")

    # Get ALL the parents of node
    for _, _, parent in graph.triples((uri_ref, RDFS.subClassOf, None)):
        parent_info = get_basic_node_info(parent, graph)

        # If ignoring deprecated nodes and a node has a deprecation date, then skip it
        if not dep and parent_info.get("dep"):
            continue

        # Add the 'has_parents' field
        if parent_flag:
            parent_info["has_parents"] = has_parents(str(parent), graph, dep)

        # Incriment number of parents since it has now been included as a parent
        num_parents += 1

        # Obtain the children of the parents ONLY if requested
        if include_ex_children:
            parent_info["extra_children"] = get_children(
                uri=parent,
                graph=graph,
                dep=dep,
                ex_parents=children_ex_parents,
                children_flag=False,  # Dont include attribute in children of parents
                order=order,
                ignore_id=uri,
            )

        # Append the parent to the hierarchy
        hierarchy.append(parent_info)

    # Order the children by their label if 'order' is set to True
    if order:
        hierarchy.sort(key=lambda x: (x.get("label") or ""))

    return hierarchy


def get_local_hierarchy_to_root(
    uri: str,
    graph,
    dep: bool = False,
    ex_parents: bool = True,
    children_flag: bool = True,
    parent_flag: bool = False,
    order: bool = True,
    include_children: bool = True,
) -> list[dict[str, any]]:
    """
    Get the local hierarchy of a node from the root all the way to the selected node,
    only including the children and parents required to get to the node.

    Args:
        uri (str): The URI of the node to retrieve the hierarchy for.
        graph (rdflib.Graph): The RDFLib graph to query.
        dep (bool, optional): Whether to include deprecated nodes (default: False).
        ex_parents (bool, optional): Whether to include extra parents (multi-parent) (default: True).
        children_flag (bool, optional): Whether to include a flag indicating if the node has children (default: True).
        parent_flag (bool, optional): Whether to include a flag indicating if the node has parents (default: True).
        order (bool, optional): Whether to order children alphabetically by label (default: True).
        include_children (bool, optional): Whether to include the direct children of the selected node (default: True).

    Returns:
        list[dict]: A list representing the hierarchy, with the node's children placed correctly under its parents.
    """
    if not check_uri_exists(uri=uri, graph=graph):
        raise ValueError(f"URI '{uri}' does not exist within the database")

    node_list = []
    children = []

    # Create the initial structure for the centre node
    centre_node = get_basic_node_info(uri=uri, graph=graph)
    centre_node["centre"] = True  # Mark this as the centre node
    node_list.append(uri)  # Add centre node in node list

    # Start by getting the children of the centre node (if requested)
    if include_children:
        children = get_children(
            uri=uri,
            graph=graph,
            dep=dep,
            ex_parents=ex_parents,
            children_flag=children_flag,
            order=order,
            ignore_id=uri,  # Prevent the node to be a child of itself
        )
        centre_node["children"] = children  # Add the node's children

    # Add the children to the list
    for child in children:
        node_list.append(child.get("id"))

    # Add the 'has_children' field
    if children_flag:
        centre_node["has_children"] = has_children(uri=str(uri), graph=graph, dep=dep)

    # Now get the parents of the centre node
    parents = get_parents(
        uri=uri,
        graph=graph,
        dep=dep,
        ex_parents=ex_parents,
        children_flag=children_flag,
        parent_flag=parent_flag,
        order=order,
        include_children=False,  # Don't include children at the parent level yet
    )

    # If the node has no parents, return the centre node structure as it is the root
    if not parents:
        return centre_node

    # Add the parents' IDs to the node_list
    for parent in parents:
        node_list.append(parent["id"])

    # Select the first parent to append the structure to
    main_parent = parents[0]

    # If the node has additional parents, add them to the 'extra_parents' field
    if ex_parents and len(parents) > 1:
        centre_node["extra_parents"] = [{"id": parent["id"]} for parent in parents[1:]]

    # Start building from the first parent up to the root
    hierarchy = build_parent_hierarchy(
        node=centre_node,
        node_list=node_list,
        parent_uri=main_parent["id"],
        graph=graph,
        dep=dep,
        ex_parents=ex_parents,
        parent_flag=parent_flag,
        order=order,
    )

    return hierarchy


def build_parent_hierarchy(
    node: dict,
    parent_uri: str,
    graph,
    node_list: list,
    dep: bool = False,
    ex_parents: bool = True,
    parent_flag: bool = False,
    order: bool = True,
) -> dict:
    """
    Recursively builds the parent hierarchy by appending the current node structure to its parent.

    This function recursively traverses the graph from a given node upwards to the root, building a hierarchy
    of nodes and their relationships. It appends the current node's structure as a child to its parent,
    and continues to go up through the graph, attaching parents until it reaches the root.

    Args:
        node (dict): The current node's structure, including children and other relevant information.
        parent_uri (str): The URI of the parent node to which the current node will be attached.
        graph (rdflib.Graph): The RDFLib graph that stores the relationships between nodes.
        node_list (list): A list of node URIs that have already been processed, used to avoid duplication.
        dep (bool, optional): Whether to include deprecated nodes in the hierarchy (default: False).
        ex_parents (bool, optional): Whether to include additional parents (multi-parent scenario) (default: True).
        parent_flag (bool, optional): Whether to include a flag indicating if the node has parents (default: False).
        order (bool, optional): Whether to order children alphabetically by label (default: True).

    Returns:
        dict: A dictionary representing the hierarchical structure, with the current node attached to its parent
              and any additional parents or children included as necessary.
    """
    # Get the parents of the current parent node
    parent_structure = get_basic_node_info(uri=parent_uri, graph=graph)
    parent_structure["children"] = [
        node
    ]  # The current node becomes a child of this parent

    if ex_parents:
        # Get children that match node_list and add them to the parent's children
        matching_children = get_children(
            uri=parent_uri,
            graph=graph,
            dep=dep,
            ex_parents=ex_parents,
            children_flag=False,
            order=order,
            inclusion_list=node_list,  # Include ONLY the drawn nodes to check for multi-parent links
            ignore_id=node["id"],  # Ignore the current node to avoid duplication
        )

        # Add matching children from node_list to the parent
        parent_structure["children"].extend(matching_children)

    parents_of_parent = get_parents(
        uri=parent_uri,
        graph=graph,
        dep=dep,
        ex_parents=ex_parents,
        children_flag=False,
        parent_flag=parent_flag,
        order=order,
        include_children=False,
    )

    # If there are parents, go up another level
    if parents_of_parent:
        main_parent = parents_of_parent[0]

        # Add extra parents if there are any
        if ex_parents and len(parents_of_parent) > 1:
            parent_structure["extra_parents"] = [
                {"id": p["id"]} for p in parents_of_parent[1:]
            ]

        # Add the parents' IDs to the node_list
        for parent in parents_of_parent:
            node_list.append(parent["id"])

        # Recursively add the parent structure
        parent_structure = build_parent_hierarchy(
            node=parent_structure,
            parent_uri=main_parent["id"],
            node_list=node_list,
            graph=graph,
            dep=dep,
            ex_parents=ex_parents,
            parent_flag=parent_flag,
            order=order,
        )

    return parent_structure


#  Convert a string to a boolean and accepts common representations of true/false.
def str_to_bool(value: str) -> bool:
    """
    Converts a string to a boolean, accepting common representations of true/false.

    Args:
        value (str or any): The value to convert to boolean.

    Returns:
        bool: True if the string is a truthy value ('true', '1', 't', 'y', 'yes'), otherwise False.
    """
    if isinstance(value, str):
        return value.lower() in ["true", "1", "t", "y", "yes"]
    return bool(value)
