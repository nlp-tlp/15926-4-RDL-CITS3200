from rdflib import URIRef
from app.controllers import get_root_node_info, get_children, check_uri_exists


def test_uri_check(sample_graph):
    """
    Test that the RDFLib graph is initialized with expected triples.
    """
    root_node = URIRef("http://data.15926.org/dm/Thing")
    assert check_uri_exists(
        str(root_node), sample_graph
    ), "Root node should exist in the graph."


def test_get_root_node_info(sample_graph):
    """
    Test the get_root_node_info function from controllers.py.
    """
    # Call get_root_node_info with the sample graph
    root_info = get_root_node_info(sample_graph)

    # Validate the root node info
    assert root_info["id"] == "http://data.15926.org/dm/Thing"
    assert root_info["label"] == "Thing"
    assert root_info["dep"] is None, "Root node should not have a deprecation date."


def test_get_children(sample_graph):
    """
    Test the get_children function from controllers.py.
    """
    # Get the children of the root node
    root_node = "http://data.15926.org/dm/Thing"
    children = get_children(root_node, sample_graph)

    # Validate that the correct children are returned
    assert len(children) == 2, "Root node should have 2 children."

    child_ids = {child["id"] for child in children}
    assert "http://data.15926.org/dm/Child1" in child_ids
    assert "http://data.15926.org/dm/Child2" in child_ids

    # Validate the deprecation date for Child1
    for child in children:
        if child["id"] == "http://data.15926.org/dm/Child1":
            assert (
                child["dep"] == "2021-03-21Z"
            ), "Child1 should have a deprecation date."
        else:
            assert child["dep"] is None, "Child2 should not have a deprecation date."


def test_check_uri_exists(sample_graph):
    """
    Test the check_uri_exists function from controllers.py.
    """
    # Test with a valid URI
    root_node = "http://data.15926.org/dm/Thing"
    assert check_uri_exists(root_node, sample_graph), "Root node should exist."

    # Test with an invalid URI
    invalid_uri = "http://data.15926.org/dm/NonExistentNode"
    assert not check_uri_exists(
        invalid_uri, sample_graph
    ), "Non-existent URI should not exist."
