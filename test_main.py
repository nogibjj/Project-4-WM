from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
       "message": "This api will show the sentiment of a subreddit of your choice."
    }

def test_read_subreddit():
    response = client.get("/top_three/soccer")
    assert response.status_code == 200