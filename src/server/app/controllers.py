from app.config import Config
from rdflib import URIRef, Literal, RDF, RDFS, Namespace
from rapidfuzz import process, fuzz

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
            definition = str(obj)
            definition = definition.replace("&lt;", "<").replace("&gt;", ">")
            node_info["definition"] = definition

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

            # Append the child info to the children list
            children_list.append(child_info)

    # Order the children by their label if 'order' is set to True
    if order:
        children_list.sort(key=lambda x: (x.get("label") or ""))

    return children_list


def search(search_key, field, graph, dep=False, limit=5, min_similarity=75):
    """
    Search the RDFLib graph for nodes by URI or label, with optional filtering for deprecated nodes.
    Return results within the limit and ranked by relavence to the search key.

    Args:
        search_key (str): The search term (either part of a URI or part of a label).
        field (str): The field to search by ('URI' or 'LABEL').
        graph (rdflib.Graph): The RDFLib graph to query.
        dep (bool, optional): Whether to include deprecated nodes. Defaults to False.
        limit (int, optional): Maximum number of results to return. Defaults to 5.
        min_similarity (int, optional): Minimum similarity score of results to return. Default to 75(%).

    Returns:
        list: A list of unique dictionaries containing node information.
    """
    # Initialise results array
    results = []

    # Ensure case insensitivity by lowering the search key
    search_key_lower = search_key.lower()

    # NOTE: The search ranking must be performed with case insensitivity, however the information must
    # be obtained using the original case sensitive URI, so the original must be stored as well.

    # Check if the field is "LABEL"
    if field.upper() == "LABEL":

        labels = set()  # Ensure unique labels to prevent duplication
        uri_label_map = {}  # Map labels to their URIs

        for uri, _, label in graph.triples((None, RDFS.label, None)):
            if isinstance(label, Literal):
                label = str(label).lower()  # Ensure case insensitivity
                labels.add(label)
                uri_label_map[label] = uri  # Store original URI with lowercase label

        # Find similar matches based on the label
        matches = process.extract(
            search_key_lower,
            list(labels),
            scorer=fuzz.WRatio,
            limit=limit,
            score_cutoff=min_similarity,
        )

        for label, _, _ in matches:
            uri = uri_label_map[label]

            # Get basic node info
            node_info = get_basic_node_info(uri=uri, graph=graph)

            # Skip if we don't want deprecated nodes
            if not dep and node_info.get("dep"):
                continue

            results.append(node_info)

    # Default or explicit "URI" search (substring match)
    else:
        # Get all URIs in the graph, preserving original URIs in a map for case insensitivity
        uri_map = {str(uri).lower(): uri for uri in graph.subjects()}

        # Perform case-insensitive search on lowercase URIs
        uris = list(uri_map.keys())

        # Find similar matches using a list of the uris
        # Use custom scorer to put more emphasis on numbers in the id
        matches = process.extract(
            search_key_lower,
            list(uris),
            scorer=custom_number_sensitive_scorer,
            limit=limit,
            score_cutoff=min_similarity,
        )

        for uri_lower, _, _ in matches:
            original_uri = uri_map[uri_lower]  # Retrieve original case-sensitive URI
            node_info = get_basic_node_info(uri=original_uri, graph=graph)

            if not dep and node_info.get("dep"):
                continue

            results.append(node_info)

    return results


def custom_number_sensitive_scorer(search_key, candidate, **kwargs):
    """
    Custom scorer that gives more weight to numeric parts of the string
    by combining WRatio and partial_ratio for exact numeric matching.
    Accepts arbitrary keyword arguments to handle RapidFuzz's internal kwargs.
    """
    # Apply WRatio for general matching
    w_ratio_score = fuzz.WRatio(search_key, candidate)

    # Apply partial_ratio to boost exact matches of substrings, especially numbers
    partial_score = fuzz.partial_ratio(search_key, candidate)

    # Emphasize numbers using partial_ratio, then combine with WRatio
    combined_score = (w_ratio_score * 0.6) + (partial_score * 0.4)

    return combined_score


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
