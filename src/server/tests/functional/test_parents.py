def test_parents(test_client):
    """
    Test the parents endpoint by checking if the correct parents of a node are returned.
    """
    # Request the parents for 'Child Two'
    response = test_client.get("/node/parents/http://data.15926.org/dm/Child2")

    assert response.status_code == 200
    data = response.get_json()

    # Check the structure of the response
    assert data["id"] == "http://data.15926.org/dm/Child2"
    assert "hierarchy" in data

    # Check that the parents are correct
    hierarchy = data["hierarchy"]
    parent_labels = [parent["label"] for parent in hierarchy]

    # Verify that the correct parents are included
    assert "Thing" in parent_labels
    assert "Another Parent" in parent_labels


def test_parents_with_deprecated(test_client):
    """
    Test the parents endpoint with the option to include deprecated nodes.
    """

    # Request the parents for 'Child One', including deprecated nodes
    response = test_client.get("/node/parents/http://data.15926.org/dm/Child1?dep=true")

    assert response.status_code == 200
    data = response.get_json()

    # Check the structure of the response
    assert data["id"] == "http://data.15926.org/dm/Child1"
    assert "hierarchy" in data

    # Check that the parents are correct
    hierarchy = data["hierarchy"]
    parent_labels = [parent["label"] for parent in hierarchy]

    # Verify that the correct parents are included
    assert "Thing" in parent_labels

    # Check that deprecated nodes are included
    deprecated_ids = []
    for parent in hierarchy:
        for child in parent.get("children"):
            if child.get("dep"):
                deprecated_ids.append(child.get("id"))
    assert "http://data.15926.org/dm/Child1" in deprecated_ids
