from app import app                       # load your Flask app from app.py

def test_home_page():
    client = app.test_client()            # the fake browser
    response = client.get("/")            # visit /
    assert response.status_code == 200    # check 1: the status code/ the page loaded successfully
    assert response.text.startswith("localhost:8080/")  # check 2: the reply text is right