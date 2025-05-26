import pytest
from monik.app import create_app

@pytest.fixture
def client():
    app = create_app("product")
    app.config["TESTING"] = True
    return app.test_client()

def test_report_route(client):
    response = client.get("/report")
    assert response.status_code == 200
    assert response.is_json

def test_cron_nodata_route(client):
    response = client.get("/cron-nodata")
    assert response.status_code == 200
    assert response.is_json

def test_upload_route(client):
    response = client.get(
        "/upload",
        headers={
            "checkname": "meta",
            "status": "0",
            "description": "OK",
            "Hostname": "test",
            "ttl": "60"
        }
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.is_json, "Response is not JSON"
    assert response.get_json() == {"success": True}, f"Unexpected response body: {response.get_json()}"

def test_downtime_route(client):
    response = client.get(
        "/downtime",
        headers={
            "checkname": "meta",
            "hostname": "test",
            "downtime_secs": "60"
        }
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.is_json, "Response is not JSON"
    assert response.get_json() == {"success": True}, f"Unexpected response body: {response.get_json()}"

def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<html" in response.data  # crude check for HTML
