import pytest
from app import create_app
from app.config import TestConfig
from rdflib import Graph, Namespace, Literal, URIRef, RDFS


# Define the namespace for your test data
META = Namespace("http://data.15926.org/meta/")


@pytest.fixture(scope="module")
def sample_graph():
    """
    Create and populate a sample RDFLib graph with test data.
    This simulates a small sample database.
    """
    graph = Graph()

    # Sample nodes (URIs)
    root_node = URIRef("http://data.15926.org/dm/Thing")
    child1 = URIRef("http://data.15926.org/dm/Child1")
    child2 = URIRef("http://data.15926.org/dm/Child2")

    # Add triples to the graph
    graph.add((root_node, RDFS.label, Literal("Thing")))
    graph.add((child1, RDFS.label, Literal("Child One")))
    graph.add((child2, RDFS.label, Literal("Child Two")))

    # Add subclass relationships (children)
    graph.add((child1, RDFS.subClassOf, root_node))
    graph.add((child2, RDFS.subClassOf, root_node))

    # Add deprecation date for one of the children
    graph.add((child1, META.valDeprecationDate, Literal("2021-03-21Z")))

    return graph


@pytest.fixture(scope="module")
def test_client(sample_graph):
    # Set up a test client using the TestConfig
    flask_app = create_app(TestConfig)

    # Inject the sample graph into the application context
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            # Set the graph in the Flask application context (assumes current_app.graph is used)
            flask_app.graph = sample_graph  # Assign the graph to the current app

            yield testing_client  # Yield the test client to the test functions
