def test_get_children_with_default_deprecation(test_client):
    """
    Test the '/graph/children' route to fetch the children of the root node.
    With dep=False by default, it should exclude Child1 (which has a deprecation date).
    """
    # Send a request to the /graph/children route with the root node's URI (default dep=False)
    response = test_client.get("/graph/children/http://data.15926.org/dm/Thing")

    # Parse the JSON response
    data = response.get_json()

    # Assert that the response contains the correct children
    assert response.status_code == 200
    assert "children" in data

    # Child1 should be excluded since dep=False by default
    assert len(data["children"]) == 1  # Expect only 1 child (Child2)
    assert data["children"][0]["label"] == "Child Two"


def test_get_children_without_deprecation(test_client):
    """
    Test the '/graph/children' route to fetch the children of the root node.
    With dep=False, it should exclude Child1 (which has a deprecation date).
    """
    # Send a request to the /graph/children route with the root node's URI (default dep=False)
    response = test_client.get(
        "/graph/children/http://data.15926.org/dm/Thing?dep=false"
    )

    # Parse the JSON response
    data = response.get_json()

    # Assert that the response contains the correct children
    assert response.status_code == 200
    assert "children" in data

    # Child1 should be excluded since dep=False by default
    assert len(data["children"]) == 1  # Expect only 1 child (Child2)
    assert data["children"][0]["label"] == "Child Two"


def test_get_children_with_deprecation(test_client):
    """
    Test the '/graph/children' route to fetch the children of the root node with dep=True.
    Both Child1 (with a deprecation date) and Child2 should be included.
    """
    # Send a request to the /graph/children route with the root node's URI and dep=True
    response = test_client.get(
        "/graph/children/http://data.15926.org/dm/Thing?dep=true"
    )

    # Parse the JSON response
    data = response.get_json()

    # Assert that the response contains the correct children
    assert response.status_code == 200
    assert "children" in data
    assert len(data["children"]) == 2  # Expect 2 children (Child1 and Child2)

    # Validate Child1
    child1_info = next(
        (
            child
            for child in data["children"]
            if child["id"] == "http://data.15926.org/dm/Child1"
        ),
        None,
    )
    assert child1_info is not None
    assert child1_info["label"] == "Child One"
    assert child1_info["dep"] == "2021-03-21Z"  # Child1 has a deprecation date

    # Validate Child2
    child2_info = next(
        (
            child
            for child in data["children"]
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
    response = test_client.get(f"/graph/children/{invalid_uri}")

    # Parse the JSON response
    data = response.get_json()

    # Assert that the response contains an error message
    assert response.status_code == 404
    assert "error" in data
    assert data["error"] == f"URI '{invalid_uri}' does not exist within the database"


def test_get_children_with_extra_parents(test_client):
    """
    Test the '/graph/children' route to fetch the children of the root node.
    Ensure that the 'extra_parents' field is included for nodes with multiple parents.
    """
    # Send a request to the /graph/children route with the root node's URI
    response = test_client.get(
        "/graph/children/http://data.15926.org/dm/Thing?dep=true&ex_parents=true"
    )

    # Parse the JSON response
    data = response.get_json()

    # Assert that the response contains the correct children
    assert response.status_code == 200
    assert "children" in data

    # There should be 2 children (Child1 and Child2)
    assert len(data["children"]) == 2

    # Validate Child2, which should have an extra parent (AnotherParent)
    child2_info = next(
        (
            child
            for child in data["children"]
            if child["id"] == "http://data.15926.org/dm/Child2"
        ),
        None,
    )
    assert child2_info is not None
    assert child2_info["label"] == "Child Two"
    assert "extra_parents" in child2_info
    assert len(child2_info["extra_parents"]) == 1
    assert (
        child2_info["extra_parents"][0]["id"] == "http://data.15926.org/dm/ExtraParent"
    )

    # Validate that Child1 does not have extra parents
    child1_info = next(
        (
            child
            for child in data["children"]
            if child["id"] == "http://data.15926.org/dm/Child1"
        ),
        None,
    )
    assert child1_info is not None
    assert "extra_parents" not in child1_info


def test_get_node_info(test_client):
    """
    Test that the node information retrieved via the '/node/info' endpoint includes label, types,
    deprecation date, definition, and properties.
    """
    # Node URI for the test
    node_uri = "http://data.15926.org/dm/Child1"

    # Send a request to the '/node/info' endpoint with the node URI
    response = test_client.get(f"/node/info/{node_uri}")
    json_data = response.get_json()

    # Assert the basic fields are correct
    assert response.status_code == 200
    assert json_data["id"] == node_uri
    assert json_data["label"] == "Child One"
    assert json_data["dep"] == "2021-03-21Z"  # Child1 has a deprecation date

    # Check types
    assert "http://data.15926.org/dm/ChildType" in json_data["types"]
    assert "http://data.15926.org/dm/AnotherType" in json_data["types"]

    # Check definition
    assert json_data["definition"] == "Child One is a sample node."

    # Ensure no custom properties were added for this node
    assert "properties" in json_data
    assert len(json_data["properties"]) == 0  # No custom properties added to Child1


def test_get_all_root_node_info_with_properties(test_client):
    """
    Test that the root node information retrieved via the '/node/info' endpoint includes label, types,
    properties, and no deprecation date.
    """
    # Node URI for the root node
    node_uri = "http://data.15926.org/dm/Thing"

    # Send a request to the '/node/info' endpoint with the root node URI
    response = test_client.get(f"/node/info/{node_uri}?all_info=true")
    json_data = response.get_json()

    # Assert the basic fields are correct
    assert response.status_code == 200
    assert json_data["id"] == node_uri
    assert json_data["label"] == "Thing"
    assert json_data["dep"] is None  # Root node does not have a deprecation date

    # Check type
    assert "http://data.15926.org/dm/RootType" in json_data["types"]

    # Check custom properties
    assert "http://example.org/hasProperty" in json_data["properties"]
    assert "Some property" in json_data["properties"]["http://example.org/hasProperty"]

    # Ensure no definition was added for the root node
    assert json_data["definition"] is None
