def test_health_check(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/ping' page is requested (GET)
    THEN check that the response is valid
    """
    # Get the response
    response = test_client.get('/ping')
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data['status'] == 'success'
    assert json_data['message'] == 'Pong!'