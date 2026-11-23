from app import app                    # load your Flask app from app.py
import fakeredis
import app as app_module



def test_home_page():
    client = app.test_client()            # the fake browser
    response = client.get("/")            # visit /
    assert response.status_code == 200    # check 1: the status code/ the page loaded successfully
    assert response.text.startswith("localhost:8080/")  # check 2: the reply text is right

def test_shorten_new_link():
    # Arrange: swap the real Redis for the dummy
    fake_r = fakeredis.FakeRedis(decode_responses=True)
    app_module.r = fake_r
    client = app.test_client()
    # Act: send a URL like a form would
    response = client.post("/shorten", data={"url": "https://github.com/jxcarter92"})
    # Assert: check what came out   
    code = response.text.strip()
    assert response.status_code == 200
    assert len(code) == 6
    assert fake_r.get(code) == "https://github.com/jxcarter92"