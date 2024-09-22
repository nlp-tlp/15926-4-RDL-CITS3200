def test_search_by_id(test_client, sample_graph):
    """
    Test the '/search/id' route to search for a node by its URI.
    """
    node_uri = "http://data.15926.org/dm/Thing"
    response = test_client.get(f"/search/id/{node_uri}?limit=5&dep=False")
    json_data = response.get_json()

    # Assert the response is valid and the node exists
    assert response.status_code == 200
    assert json_data["id"] == node_uri
    assert len(json_data["results"]) > 0  # Ensure results are returned

    # Check that the node exists in the results
    result_ids = [result["id"] for result in json_data["results"]]
    assert node_uri in result_ids


def test_search_by_id_no_results(test_client):
    """
    Test the '/search/id' route when the search yields no results.
    """
    invalid_node_uri = "http://data.15926.org/dm/NonExistentNode"
    response = test_client.get(f"/search/id/{invalid_node_uri}?limit=5&dep=False")
    json_data = response.get_json()

    # Assert that no results are returned
    assert response.status_code == 200
    assert json_data["id"] == invalid_node_uri
    assert len(json_data["results"]) == 0  # Ensure no results are returned


def test_search_by_label(test_client, sample_graph):
    """
    Test the '/search/label' route to search for a node by its label.
    """
    node_label = "Thing"
    response = test_client.get(f"/search/label/{node_label}?limit=5&dep=False")
    json_data = response.get_json()

    # Assert the response is valid and the node with the label exists
    assert response.status_code == 200
    assert json_data["label"] == node_label
    assert len(json_data["results"]) > 0  # Ensure results are returned

    # Check that the node with the label exists in the results
    result_labels = [result["label"] for result in json_data["results"]]
    assert node_label in result_labels


def test_search_by_label_no_results(test_client):
    """
    Test the '/search/label' route when the search yields no results.
    """
    invalid_label = "NonExistentLabel"
    response = test_client.get(f"/search/label/{invalid_label}?limit=5&dep=False")
    json_data = response.get_json()

    # Assert that no results are returned
    assert response.status_code == 200
    assert json_data["label"] == invalid_label
    assert len(json_data["results"]) == 0  # Ensure no results are returned
