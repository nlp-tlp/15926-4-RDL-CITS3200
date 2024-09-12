from .config import Config
from rdflib import URIRef, RDFS


def get_root_node():
    return Config.ROOT_NODE_URI


def get_children(uri, graph):
    children = set()  # Ensure unique children
    uri_ref = URIRef(uri)  # Convert the URI string to an RDFLib URIRef object

    # Query the graph for triples where the given URI is an object of rdfs:subClassOf
    for child, predicate, parent in graph.triples((None, RDFS.subClassOf, uri_ref)):
        children.add(child)

    return list(children)  # Convert the set to a list before returning
