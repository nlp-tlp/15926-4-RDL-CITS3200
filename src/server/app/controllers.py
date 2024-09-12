from .config import Config
from rdflib import URIRef, RDFS, Literal


def get_root_node():
    return Config.ROOT_NODE_URI


def get_children(uri, graph):
    children_set = set()  # Keep only unique children
    children_list = []
    uri_ref = URIRef(uri)  # Convert the URI string to an RDFLib URIRef object

    # Query the graph for triples where the given URI is an object of rdfs:subClassOf
    for child, predicate, parent in graph.triples((None, RDFS.subClassOf, uri_ref)):
        if child not in children_set:
            # Add the child to the set to ensure uniqueness
            children_set.add(child)

            # Dictionary to store child data
            child_info = {"id": str(child), "label": None, "dep": None}

            # Query for the label of the child
            label = None
            for _, _, label in graph.triples((child, RDFS.label, None)):
                if isinstance(label, Literal):
                    child_info["label"] = str(label)

            # Query for the deprecation date
            deprecation_date = None
            for _, _, deprecation_date in graph.triples(
                (child, URIRef("http://data.15926.org/meta/valDeprecationDate"), None)
            ):
                if isinstance(deprecation_date, Literal):
                    child_info["dep"] = str(deprecation_date)

            # Append the child info to the result list
            children_list.append(child_info)

    return children_list
