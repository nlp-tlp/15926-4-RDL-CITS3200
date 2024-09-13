def test_health_check(test_client):
    """
    Use a GET request to route '/ping' to check the response is valid.
    Valid results: (code=200, status='success', message='Pong!')
    """
    # Get the response
    response = test_client.get("/ping")
    json_data = response.get_json()

    # Validate the response
    assert response.status_code == 200
    assert json_data["status"] == "success"
    assert json_data["message"] == "Pong!"


def test_graph_root_route(test_client):
    """
    Test the /graph/root route to ensure it returns the correct root node information.
    """
    response = test_client.get("/graph/root")
    json_data = response.get_json()

    # Assert correct response for the root node
    assert response.status_code == 200
    assert json_data["id"] == "http://data.15926.org/dm/Thing"
    assert json_data["label"] == "Thing"


def test_graph_children_route(test_client):
    """
    Test the '/graph/children' route with a valid ID.
    """
    node_uri = "http://data.15926.org/dm/Thing"
    response = test_client.get(f"/graph/children/{node_uri}")
    json_data = response.get_json()

    # Assert correct response for children of the root node
    assert response.status_code == 200
    assert json_data["id"] == node_uri
    assert "children" in json_data
    assert len(json_data["children"]) > 0  # Ensure children exist


def test_graph_children_route_missing_id(test_client):
    """
    Test the '/graph/children' route without providing an ID in the query parameters.
    """
    response = test_client.get("/graph/children/")
    json_data = response.get_json()

    # Assert the response is a 400 Bad Request due to missing ID/URI
    assert response.status_code == 400
    assert "error" in json_data
    assert json_data["error"] == "ID/URI not provided. Must use '/graph/children/<id>'"
