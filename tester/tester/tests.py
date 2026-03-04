import json

def test_status_ok(client):
    response, _ = client.get("/?name=michael")
    assert response is not None
    assert response.status_code == 200

def test_json_valid(client):
    response, _ = client.get("/?name=michael")
    json.loads(response.text)

def test_fields_present(client):
    response, _ = client.get("/?name=michael")
    data = response.json()
    assert "name" in data
    assert "age" in data
    assert "count" in data

def test_types(client):
    response, _ = client.get("/?name=michael")
    data = response.json()
    assert isinstance(data["name"], str)
    assert isinstance(data["age"], int) or data["age"] is None
    assert isinstance(data["count"], int)

def test_error_empty_name(client):
    response, _ = client.get("/?name=")
    assert response.status_code in [400, 422, 200]

def test_timeout(client):
    client.timeout = 0.00001
    response, latency = client.get("/?name=michael")
    assert response is None
