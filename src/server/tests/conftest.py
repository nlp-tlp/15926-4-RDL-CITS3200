import pytest
from app import create_app
from app.config import TestConfig
from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS


# Define the namespace for your test data
META = Namespace("http://data.15926.org/meta/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")


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
    extra_parent = URIRef("http://data.15926.org/dm/ExtraParent")
    child3 = URIRef("http://data.15926.org/dm/Child3")

    # Add labels
    graph.add((root_node, RDFS.label, Literal("Thing")))
    graph.add((child1, RDFS.label, Literal("Child One")))
    graph.add((child2, RDFS.label, Literal("Child Two")))
    graph.add((child3, RDFS.label, Literal("Child Three")))
    graph.add((extra_parent, RDFS.label, Literal("Another Parent")))

    # Add subclass relationships (children)
    graph.add((child1, RDFS.subClassOf, root_node))
    graph.add((child2, RDFS.subClassOf, root_node))

    # Add subclass relationship for another parent
    graph.add((child2, RDFS.subClassOf, extra_parent))
    graph.add((child3, RDFS.subClassOf, child1))  # Make child3 a subclass of child1

    # Add deprecation date for one of the children
    graph.add((child1, META.valDeprecationDate, Literal("2021-03-21Z")))

    # Add types to the nodes
    graph.add((root_node, RDF.type, URIRef("http://data.15926.org/dm/RootType")))
    graph.add((child1, RDF.type, URIRef("http://data.15926.org/dm/ChildType")))
    graph.add((child1, RDF.type, URIRef("http://data.15926.org/dm/AnotherType")))

    # Add a skos:definition to one of the nodes
    graph.add((child1, SKOS.definition, Literal("Child One is a sample node.")))
    graph.add((child2, SKOS.definition, Literal("Child Two definition.")))

    # Add custom properties
    graph.add(
        (root_node, URIRef("http://example.org/hasProperty"), Literal("Some property"))
    )

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
