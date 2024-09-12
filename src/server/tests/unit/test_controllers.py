from rdflib import URIRef
from app.controllers import (
    get_root_node_info,
    get_children,
    check_uri_exists,
    str_to_bool,
)


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


def test_get_children_without_deprecation(sample_graph):
    """
    Test get_children with dep=False (default) to exclude deprecated nodes.
    """
    # Get children of the root node with default dep=False
    children = get_children("http://data.15926.org/dm/Thing", sample_graph, dep=False)

    # Validate that only Child2 is returned (Child1 has a deprecation date)
    assert len(children) == 1, "Only Child2 should be returned when dep=False."
    assert children[0]["id"] == "http://data.15926.org/dm/Child2"
    assert children[0]["dep"] is None, "Child2 should not have a deprecation date."


def test_get_children_with_deprecation_included(sample_graph):
    """
    Test get_children with dep=True to include deprecated nodes.
    """
    # Get the children of the root node with dep=True
    children = get_children("http://data.15926.org/dm/Thing", sample_graph, dep=True)

    # Validate that both children are returned
    assert len(children) == 2, "Root node should have 2 children when dep=True."

    # Check child IDs and deprecation dates
    child_ids = {child["id"] for child in children}
    assert "http://data.15926.org/dm/Child1" in child_ids
    assert "http://data.15926.org/dm/Child2" in child_ids

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
    assert check_uri_exists(
        "http://data.15926.org/dm/Thing", sample_graph
    ), "Root node should exist."

    # Test with an invalid URI
    assert not check_uri_exists(
        "http://data.15926.org/dm/NonExistentNode", sample_graph
    ), "Non-existent URI should not exist."


def test_str_to_bool():
    """
    Test the str_to_bool function with various inputs to verify correct behavior.
    """

    # Test truthy string values
    assert str_to_bool("true") is True
    assert str_to_bool("1") is True
    assert str_to_bool("t") is True
    assert str_to_bool("y") is True
    assert str_to_bool("yes") is True
    assert str_to_bool("True") is True  # Test case insensitivity
    assert str_to_bool("YES") is True  # Test case insensitivity

    # Test falsy string values
    assert str_to_bool("false") is False
    assert str_to_bool("0") is False
    assert str_to_bool("f") is False
    assert str_to_bool("n") is False
    assert str_to_bool("no") is False
    assert str_to_bool("False") is False  # Test case insensitivity
    assert str_to_bool("NO") is False  # Test case insensitivity

    # Test non-string values
    assert str_to_bool(True) is True  # Boolean True remains True
    assert str_to_bool(False) is False  # Boolean False remains False
    assert str_to_bool(1) is True  # Integer 1 is considered True
    assert str_to_bool(0) is False  # Integer 0 is considered False
    assert str_to_bool(None) is False  # None is considered False

    # Test invalid values
    assert str_to_bool("invalid") is False  # Any non-truthy string should be False
