from fastapi.testclient import TestClient
from fastapi import status
from main import app
# relative import
# from ..main import app  

client = TestClient(app)

def test_active_status_check():
    res = client.get("/active-status")

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {"status": "active"}