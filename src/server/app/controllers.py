from .config import Config
from rdflib import URIRef, RDFS, Literal, Namespace

# Define the namespace for deprecation date
META = Namespace("http://data.15926.org/meta/")


def get_root_node():
    return Config.ROOT_NODE_URI


def check_uri_exists(uri, graph):
    uri_ref = URIRef(uri)  # Convert the URI string to an RDFLib URIRef object

    # True if exist any tripple with URI as the subject
    return any(graph.triples((uri_ref, None, None)))


# Get only the node's LABEL and DEPRECATION DATE
def get_basic_node_info(uri, graph):
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


def get_root_node_info(graph):
    root_node_uri = get_root_node()  # Retrieve root node URI from config
    root_node_ref = URIRef(root_node_uri)  # Convert to URIRef for querying

    if not check_uri_exists(uri=root_node_uri, graph=graph):
        raise ValueError(f"URI '{root_node_uri}' does not exist within the database")

    # Use the helper function to get root node info
    return get_basic_node_info(root_node_ref, graph)


def get_children(uri, graph):
    children_set = set()  # Keep only unique children
    children_list = []
    uri_ref = URIRef(uri)  # Convert the URI string to an RDFLib URIRef object

    if not check_uri_exists(uri=uri, graph=graph):
        raise ValueError(f"URI '{uri}' does not exist within the database")

    # Query the graph for triples where the given URI is an object of rdfs:subClassOf
    for child, predicate, parent in graph.triples((None, RDFS.subClassOf, uri_ref)):
        if child not in children_set:
            children_set.add(child)  # Ensure uniqueness

            # Use the helper function to get child info
            child_info = get_basic_node_info(child, graph)
            children_list.append(child_info)

    return children_list


def get_hierarchy_below(uri, graph, dist_below, current_level=0):
    """
    Recursively fetch the hierarchy below (children) of a node.
    """
    if current_level >= dist_below:
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
        child_info["children"] = get_hierarchy_below(
            str(child), graph, dist_below, current_level + 1
        )

        children.append(child_info)

    return children


def get_hierarchy_above(uri, graph, dist_above, current_level=0):
    """
    Recursively fetch the hierarchy above (parents) of a node.
    This is not part of your example, but in case you need it later.
    """
    if current_level >= dist_above:
        return []

    parents = []
    uri_ref = URIRef(uri)

    for parent, _, _ in graph.triples((None, RDFS.subClassOf, uri_ref)):
        parent_info = {
            "id": str(parent),
            "label": get_node_label(parent, graph),
            "children": get_hierarchy_above(
                str(parent), graph, dist_above, current_level + 1
            ),
            "extra_parents": [],
        }

        parents.append(parent_info)

    return parents


def get_local_hierarchy(uri, graph, dist_below):
    """
    Get the hierarchy structure below a node.
    """
    if not check_uri_exists(uri, graph):
        raise ValueError(f"URI '{uri}' does not exist within the database")

    hierarchy = {
        "id": uri,
        "label": get_node_label(URIRef(uri), graph),
        "children": [],
        "extra_parents": [],
    }

    # Recursively get the hierarchy below the node
    hierarchy["children"] = get_hierarchy_below(uri, graph, dist_below)

    return hierarchy


def get_node_label(uri, graph):
    """
    Helper function to fetch the label of a node.
    """
    for _, _, label in graph.triples((uri, RDFS.label, None)):
        if isinstance(label, Literal):
            return str(label)
    return None
