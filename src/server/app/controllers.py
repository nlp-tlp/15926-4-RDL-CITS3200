from .config import Config
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
def get_basic_node_info(uri: str, graph) -> dict[str, any]:
    """
    Retrieves basic information about a node, including its label and deprecation date.

    Args:
        uri (str): The URI of the node to fetch information for.
        graph (rdflib.Graph): The RDFLib graph to query.

    Returns:
        dict: A dictionary containing the node's 'id', 'label', and 'dep' (deprecation date, if any).
    """
    node_info = {"id": str(uri), "label": None, "dep": None}

    # Query for the label of the node
    for _, _, label in graph.triples((uri, RDFS.label, None)):
        if isinstance(label, Literal):
            node_info["label"] = str(label)

    # Query for the deprecation date
    for _, _, deprecation_date in graph.triples((uri, META.valDeprecationDate, None)):
        if isinstance(deprecation_date, Literal):
            node_info["dep"] = str(deprecation_date)

    return node_info


# Get all information (predicates and objects) for a given node in the RDFLib graph.
def get_all_node_info(uri: str, graph, all_info: bool = True) -> dict[str, any]:
    """
    Retrieves all available information about a given node in the RDFLib graph. This includes
    specific properties such as label, types, deprecation date, definition, and parent nodes
    (subClassOf). If 'all_info' is set to True, additional properties are also returned.

    Args:
        uri (str): The URI of the node to retrieve information for.
        graph (rdflib.Graph): The RDFLib graph to query the node's information from.
        all_info (bool, optional): A flag indicating whether to retrieve additional properties (default: True).

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
    if all_info:
        node_info = {
            "id": str(uri),
            "label": None,  # Handle rdfs:label
            "types": [],  # Handle multiple rdf:type entries
            "dep": None,  # Handle meta/valDeprecationDate
            "definition": None,  # Handle skos:definition
            "parents": [],  # Handle rdfs:subClassOf
            "properties": {},  # Handle anything else
        }

    else:
        node_info = {
            "id": str(uri),
            "label": None,  # Handle rdfs:label
            "types": [],  # Handle multiple rdf:type entries
            "dep": None,  # Handle meta/valDeprecationDate
            "definition": None,  # Handle skos:definition
            "parents": [],  # Handle rdfs:subClassOf
        }

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


def get_children(
    uri: str,
    graph,
    dep: bool = False,
    ex_parents: bool = True,
    children_flag: bool = True,
    order: bool = True,
    levels: int = 1,
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
        if child not in children_set:
            # Use the helper function to get child info
            child_info = get_basic_node_info(child, graph)

            # If ignoring deprecated nodes and a node has a deprecation date, then skip it
            if not dep and child_info.get("dep"):
                continue

            # Add the child to the set and the list
            children_set.add(child)

            # Initialise an empty list for extra parents
            extra_parents_list = []

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

            # Recursively get the children's children if theres more levels to go
            if levels > 1:
                child_info["children"] = get_children(
                    uri=uri,
                    graph=graph,
                    dep=dep,
                    ex_parents=ex_parents,
                    children_flag=children_flag,
                    order=order,
                    levels=(levels - 1),
                )

            # Append the child info to the children list
            children_list.append(child_info)

    # Order the children by their label if 'order' is set to True
    if order:
        children_list.sort(key=lambda x: (x.get("label") or ""))

    return children_list


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


def get_hierarchy_below(uri, graph, dist):
    """
    Recursively fetch the hierarchy below (children) of a node.
    """
    # Once its reached the maximum depth given, return empty list
    if dist == -1:
        return []

    children = []
    uri_ref = URIRef(uri)

    for child, _, _ in graph.triples((None, RDFS.subClassOf, uri_ref)):
        child_info = {
            "id": str(child),
            "label": get_node_label(child, graph),
            "children": [],
            "extra_parents": [],
        }

        # Check for additional parents of the child
        for other_parent, _, _ in graph.triples((None, RDFS.subClassOf, child)):
            if str(other_parent) != str(uri):
                extra_parent_info = {
                    "id": str(other_parent),
                    "label": get_node_label(other_parent, graph),
                }
                child_info["extra_parents"].append(extra_parent_info)

        # Recursively get the children of this child
        child_info["children"] = get_hierarchy_below(str(child), graph, dist - 1)

        children.append(child_info)

    return children


def get_hierarchy_below(
    uri, graph, dist, dep=False, ex_parents=True, children_flag=True, order=True
):
    """
    Recursively fetch the hierarchy below (children) of a node using the get_children function.

    Args:
        uri (str): The URI of the node.
        graph (rdflib.Graph): The RDFLib graph to query.
        dist (int): The maximum depth to retrieve.
        dep (bool): Whether to include deprecated nodes.
        ex_parents (bool): Whether to include extra parents.
        children_flag (bool): Whether to include a flag indicating if the child has children.
        order (bool): Whether to order the children alphabetically.

    Returns:
        list: A list of children with their respective hierarchy.
    """
    # If we've reached the maximum depth, return an empty list
    if dist == -1:
        return []

    # Retrieve the direct children of the node using the get_children function
    children = get_children(
        uri=uri,
        graph=graph,
        dep=dep,
        ex_parents=ex_parents,
        children_flag=children_flag,
        order=order,
    )

    # Recursively retrieve children for each child node
    for child in children:
        child_uri = child["id"]
        # Recursively get the children of this child, reducing the depth by 1
        child["children"] = get_hierarchy_below(
            uri=child_uri,
            graph=graph,
            dist=dist - 1,  # Reduce the distance to ensure it caps itself
            dep=dep,
            ex_parents=ex_parents,
            children_flag=children_flag,
            order=order,
        )

    return children


def get_hierarchy_above_and_merge(
    node_uri, graph, current_hierarchy, max_height, current_level=0
):
    if current_level >= max_height:
        return current_hierarchy

    uri_ref = URIRef(node_uri)
    parents = []

    # Query for the parent nodes (rdfs:subClassOf)
    for parent, _, _ in graph.triples((None, RDFS.subClassOf, uri_ref)):
        parent_info = {
            "id": str(parent),
            "label": get_node_label(parent, graph),
            # Recursively get the parent's children and attach the known hierarchy below
            "children": current_hierarchy,
            "extra_parents": [],
        }

        # Insert the current hierarchy as one of the children of the parent
        parent_info["children"].append(current_hierarchy)

        # Add this parent to the list of parents
        parents.append(parent_info)

        # Recursively fetch the parent's parents up to the maximum height
        parent_info = get_hierarchy_above_and_merge(
            str(parent), graph, parent_info, max_height, current_level + 1
        )

    # Return the hierarchy for the parent level
    return parents


def get_local_hierarchy(uri, graph, dist_below=3, dist_above=3):
    """
    Get the hierarchy structure both below (children) and above (parents) a node.
    The function first retrieves the hierarchy below a node and then recursively
    gets the parents and their children, inserting the already known hierarchy into the parents.

    Args:
        uri (str): The URI of the node.
        graph (rdflib.Graph): The RDFLib graph to query.
        dist_below (int): The maximum depth to retrieve for children.
        dist_above (int): The maximum height to retrieve for parents.

    Returns:
        dict: The full hierarchy structure including the node itself, its children, and its ancestors' children.
    """
    if not check_uri_exists(uri, graph):
        raise ValueError(f"URI '{uri}' does not exist within the database")

    # Step 1: Get the children hierarchy below the node
    hierarchy = {
        "id": uri,
        "label": get_node_label(URIRef(uri), graph),
        "children": get_hierarchy_below(uri, graph, dist_below),
        "extra_parents": [],
    }

    # Fetch the parents and their children, inserting the hierarchy below recursively upwards
    # hierarchy["extra_parents"] = get_hierarchy_above_and_merge(uri, graph, hierarchy, dist_above)

    return hierarchy


def get_node_label(uri, graph):
    """
    Helper function to fetch the label of a node.
    """
    for _, _, label in graph.triples((uri, RDFS.label, None)):
        if isinstance(label, Literal):
            return str(label)
    return None
