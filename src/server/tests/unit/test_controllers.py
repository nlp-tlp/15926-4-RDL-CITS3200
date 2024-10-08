import pytest
from rdflib import URIRef
from app.controllers import (
    get_root_node_info,
    has_children,
    get_children,
    check_uri_exists,
    str_to_bool,
    get_all_node_info,
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
    assert "dep" not in root_info, "Root node should not have a deprecation date."


def test_has_children_without_deprecation(sample_graph):
    """
    Test has_children with dep=False (default) to exclude deprecated nodes.
    """
    # Test a non-deprecated node with non-deprecated children
    assert has_children(
        "http://data.15926.org/dm/Thing", sample_graph, dep=False
    ), "Root node should have children when dep=False."

    # Test a non-deprecated node with no children
    assert not has_children(
        "http://data.15926.org/dm/Child2", sample_graph, dep=False
    ), "Child2 should not have children when dep=False."

    # Test a non-deprecated node with deprecated children
    assert not has_children(
        "http://data.15926.org/dm/Child4", sample_graph, dep=False
    ), "Child4 should not have children when dep=False, Child5 is deprecated."


def test_has_children_with_deprecation_included(sample_graph):
    """
    Test has_children with dep=True to include deprecated nodes.
    """
    # Test a non-deprecated node with deprecated and non-deprecated children
    assert has_children(
        "http://data.15926.org/dm/Thing", sample_graph, dep=True
    ), "Root node should have children when dep=True."

    # Test a non-deprecated node with no children
    assert not has_children(
        "http://data.15926.org/dm/Child2", sample_graph, dep=True
    ), "Child2 should not have children when dep=True."

    # Test a non-deprecated node with deprecated children
    assert has_children(
        "http://data.15926.org/dm/Child4", sample_graph, dep=True
    ), "Child4 should have children when dep=True, Child5 is deprecated."


def test_get_children_without_deprecation(sample_graph):
    """
    Test get_children with dep=False (default) to exclude deprecated nodes.
    """
    # Get children of the root node with default dep=False
    children = get_children("http://data.15926.org/dm/Thing", sample_graph, dep=False)

    # Sort children by id to ensure consistent order
    children.sort(key=lambda x: x["id"])

    # Validate that only Child2 and Child4 are returned, Child1 is deprecated
    assert (
        len(children) == 2
    ), "Root node should have 2 children when dep=False, Child2 and Child4."

    assert children[0]["id"] == "http://data.15926.org/dm/Child2"
    assert "dep" not in children[0], "Child2 should not have a deprecation date."

    assert children[1]["id"] == "http://data.15926.org/dm/Child4"
    assert "dep" not in children[1], "Child4 should not have a deprecation date."


def test_get_children_with_deprecation_included(sample_graph):
    """
    Test get_children with dep=True to include deprecated nodes.
    """
    # Get the children of the root node with dep=True
    children = get_children("http://data.15926.org/dm/Thing", sample_graph, dep=True)

    # Validate that all children are returned
    assert (
        len(children) == 3
    ), "Root node should have 3 children when dep=True, Child1, Child2, and Child4."

    child_ids = {child["id"] for child in children}
    assert "http://data.15926.org/dm/Child1" in child_ids
    assert "http://data.15926.org/dm/Child2" in child_ids
    assert "http://data.15926.org/dm/Child4" in child_ids

    for child in children:
        if child["id"] == "http://data.15926.org/dm/Child1":
            assert (
                child["dep"] == "2021-03-21Z"
            ), "Child1 should have a deprecation date."
        else:
            assert (
                "dep" not in child
            ), "Child2 and Child4 should not have deprecation dates."


def test_get_children_with_extra_parents(sample_graph):
    """
    Test the get_children function from controllers.py to ensure extra parents are included correctly.
    """
    # Call get_children with ex_parents=True (default)
    children = get_children(
        "http://data.15926.org/dm/Thing", sample_graph, dep=True, ex_parents=True
    )

    # Validate that Child2 has an extra parent
    child2_info = next(
        (
            child
            for child in children
            if child["id"] == "http://data.15926.org/dm/Child2"
        ),
        None,
    )
    assert child2_info is not None, "Child2 should exist in the children list"
    assert len(child2_info["extra_parents"]) == 1, "Child2 should have 1 extra parent"

    # Validate the extra parent info
    extra_parent_info = child2_info["extra_parents"][0]
    assert (
        extra_parent_info["id"] == "http://data.15926.org/dm/ExtraParent"
    ), "Child2's extra parent should be 'Extra Parent'"


def test_get_all_node_info(sample_graph):
    """
    Test the get_all_node_info function with default all_node parameter from controllers.py.
    """
    # Test with Child1
    node_uri = "http://data.15926.org/dm/Child1"
    node_info = get_all_node_info(node_uri, sample_graph)

    # Assert the basic fields are correct
    assert node_info["id"] == node_uri
    assert node_info["label"] == "Child One"
    assert node_info["dep"] == "2021-03-21Z"  # Child1 has a deprecation date
    assert "http://data.15926.org/dm/ChildType" in node_info["types"]
    assert node_info["definition"] == "Child One is a sample node."

    # Ensure there are no extra properties for Child1
    assert "properties" in node_info
    assert len(node_info["properties"]) == 0  # No custom properties


def test_get_all_node_info_non_existent_node(sample_graph):
    """
    Test the get_all_node_info function with a non-existent node to ensure it raises a ValueError.
    """
    non_existent_node_uri = "http://data.15926.org/dm/NonExistentNode"
    with pytest.raises(
        ValueError,
        match=f"URI '{non_existent_node_uri}' does not exist within the database",
    ):
        get_all_node_info(non_existent_node_uri, sample_graph)


def test_get_all_node_info_multiple_types(sample_graph):
    """
    Test the get_all_node_info function with a node that has multiple types.
    """
    node_uri = "http://data.15926.org/dm/Child1"
    node_info = get_all_node_info(node_uri, sample_graph)

    # Assert the basic fields are correct
    assert node_info["id"] == node_uri
    assert node_info["label"] == "Child One"
    assert node_info["dep"] == "2021-03-21Z"  # Child1 has a deprecation date
    assert "http://data.15926.org/dm/ChildType" in node_info["types"]
    assert "http://data.15926.org/dm/AnotherType" in node_info["types"]
    assert node_info["definition"] == "Child One is a sample node."


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


@pytest.mark.parametrize(
    "input_value, expected_result",
    [
        # Test truthy string values
        ("true", True),
        ("1", True),
        ("t", True),
        ("y", True),
        ("yes", True),
        ("True", True),  # Test case insensitivity
        ("YES", True),  # Test case insensitivity
        # Test falsy string values
        ("false", False),
        ("0", False),
        ("f", False),
        ("n", False),
        ("no", False),
        ("False", False),  # Test case insensitivity
        ("NO", False),  # Test case insensitivity
        # Test non-string values
        (True, True),  # Boolean True remains True
        (False, False),  # Boolean False remains False
        (1, True),  # Integer 1 is considered True
        (0, False),  # Integer 0 is considered False
        (None, False),  # None is considered False
        # Test invalid values
        ("invalid", False),  # Any non-truthy string should be False
        ("", False),  # Empty string should be False
        (" ", False),  # Whitespace string should be False
        ("null", False),
        ("None", False),
    ],
)
def test_str_to_bool(input_value, expected_result):
    """
    Parameterized test for the str_to_bool function with various inputs to verify correct behavior.
    """
    assert str_to_bool(input_value) == expected_result
