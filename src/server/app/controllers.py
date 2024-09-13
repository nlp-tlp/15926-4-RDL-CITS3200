from .config import Config
from rdflib import URIRef, Literal, RDF, RDFS, Namespace

# Define the namespace for meta and SKOS
META = Namespace("http://data.15926.org/meta/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")


def get_root_node():
    """
    Retrieves the root node URI from the configuration.

    Returns:
        str: The URI of the root node from the configuration.
    """
    return Config.ROOT_NODE_URI


def check_uri_exists(uri, graph):
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
def get_basic_node_info(uri, graph):
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
def get_all_node_info(uri, graph, all_info=True):
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


def get_root_node_info(graph):
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


def get_children(uri, graph, dep=False, ex_parents=True):
    """
    Retrieves the children of a given node, with optional inclusion of deprecated nodes and extra parents.

    Args:
        uri (str): The URI of the node to fetch children for.
        graph (rdflib.Graph): The RDFLib graph to query.
        dep (bool, optional): Whether to include deprecated nodes. Defaults to False.
        ex_parents (bool, optional): Whether to include extra parents for each child. Defaults to True.

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

            # Append the child info to the children list
            children_list.append(child_info)

    return children_list


#  Convert a string to a boolean and accepts common representations of true/false.
def str_to_bool(value):
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
