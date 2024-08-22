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
