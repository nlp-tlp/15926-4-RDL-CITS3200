def test_local_hierarchy(test_client):
    """
    Test the local-hierarchy endpoint by checking if the hierarchy of a node
    includes the correct parents and children.
    """
    # Request the hierarchy for the root node 'Thing'
    response = test_client.get("/graph/local-hierarchy/http://data.15926.org/dm/Thing")

    assert response.status_code == 200
    data = response.get_json()

    # Check the structure of the response
    assert data["centre_id"] == "http://data.15926.org/dm/Thing"
    assert "hierarchy" in data

    # Check that the children are correctly included in the hierarchy
    hierarchy = data["hierarchy"]
    assert "children" in hierarchy
    children = hierarchy["children"]

    # Verify that "Child One" and "Child Two" are part of the children
    child_labels = [child["label"] for child in children]
    assert "Child One" not in child_labels
    assert "Child Two" in child_labels
    assert "Child Four" in child_labels

    # Verify that deprecated nodes are excluded by default
    deprecated_ids = []
    for parent in hierarchy.get("children"):
        if parent.get("dep"):
            deprecated_ids.append(parent.get("id"))
    assert "http://data.15926.org/dm/Child1" not in deprecated_ids


def test_local_hierarchy_with_deprecated(test_client):
    """
    Test the local-hierarchy endpoint with the option to include deprecated nodes.
    """
    # Request the hierarchy for the root node 'Thing', including deprecated nodes
    response = test_client.get(
        "/graph/local-hierarchy/http://data.15926.org/dm/Thing?dep=true"
    )

    assert response.status_code == 200
    data = response.get_json()

    # Check the structure of the response
    assert data["centre_id"] == "http://data.15926.org/dm/Thing"
    assert "hierarchy" in data

    # Check that the children include deprecated nodes
    hierarchy = data["hierarchy"]
    assert "children" in hierarchy
    children = hierarchy["children"]

    # Verify that "Child One" and "Child Two" are part of the children
    child_labels = [child["label"] for child in children]
    assert "Child One" in child_labels
    assert "Child Two" in child_labels

    # Check that deprecated nodes are included when the dep flag is set
    deprecated_ids = []
    for parent in hierarchy.get("children"):
        if parent.get("dep"):
            deprecated_ids.append(parent.get("id"))
    assert "http://data.15926.org/dm/Child1" in deprecated_ids
