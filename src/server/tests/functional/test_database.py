def test_get_children(test_client):
    """
    Test the '/graph/children' route to fetch the children of the root node.
    """
    # Send a request to the /graph/children route with the root node's URI
    response = test_client.get("/graph/children?id=http://data.15926.org/dm/Thing")

    # Parse the JSON response
    data = response.get_json()

    # Assert that the response contains the correct children
    assert response.status_code == 200
    assert "children" in data
    assert len(data["children"]) == 2  # Expect 2 children
    assert data["children"][0]["label"] == "Child One"
    assert data["children"][1]["label"] == "Child Two"


def test_get_deprecation_from_children(test_client):
    """
    Test fetching the children of the root node (Thing) and verifying the deprecation dates of Child1 and Child2.
    Using route '/graph/children'.
    """
    # Send a request to the /graph/root endpoint to get the root node's children
    response = test_client.get("/graph/children?id=http://data.15926.org/dm/Thing")

    # Parse the JSON response
    data = response.get_json()

    # Assert that the response contains the correct root node info
    assert response.status_code == 200
    assert data["id"] == "http://data.15926.org/dm/Thing"
    assert "children" in data
    assert len(data["children"]) == 2  # Should have exactly 2 children

    # Extract children information
    children = data["children"]

    # Check the first child (Child1) for label and deprecation date
    child1_info = next(
        (
            child
            for child in children
            if child["id"] == "http://data.15926.org/dm/Child1"
        ),
        None,
    )
    assert child1_info is not None
    assert child1_info["label"] == "Child One"
    assert child1_info["dep"] == "2021-03-21Z"  # Child1 has a deprecation date

    # Check the second child (Child2) for label and deprecation date
    child2_info = next(
        (
            child
            for child in children
            if child["id"] == "http://data.15926.org/dm/Child2"
        ),
        None,
    )
    assert child2_info is not None
    assert child2_info["label"] == "Child Two"
    assert child2_info["dep"] is None  # Child2 does not have a deprecation date


def test_get_root_node_info(test_client):
    """
    Test the root node information from the '/graph/root' endpoint.
    """
    response = test_client.get("/graph/root")

    # Parse the JSON response
    data = response.get_json()

    # Assert that the response contains the correct root node info
    assert response.status_code == 200
    assert data["id"] == "http://data.15926.org/dm/Thing"
    assert data["label"] == "Thing"
    assert data["dep"] is None  # Root node has no deprecation date


def test_invalid_query_to_children(test_client):
    """
    Test an invalid query to '/graph/children', where the provided URI doesn't exist.
    """
    invalid_uri = "http://data.15926.org/dm/NonExistent"
    response = test_client.get(f"/graph/children?id={invalid_uri}")

    # Parse the JSON response
    data = response.get_json()

    # Assert that the response contains an error message
    assert response.status_code == 404
    assert "error" in data
    assert data["error"] == f"URI '{invalid_uri}' does not exist within the database"
