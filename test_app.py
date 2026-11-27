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

def test_redirect():
    #Arrange:swap the real Redis for the dummy
    fake_r = fakeredis.FakeRedis(decode_responses=True)
    app_module.r = fake_r
    fake_r.set("qRNGdA", "https://spotify.com")# save one link in the dummy for the route to find. Both values have to match from /links
    client = app.test_client() # fake browser that visits the routes
    # Act: visit the short link like a browser would "qRNGdA"
    response = client.get("/qRNGdA")#check short link to see if it matches
    # Assert:check what came out  
    assert response.status_code == 302 #302 = redirect, go over there
    assert response.headers.get("Location") == "https://spotify.com"# redirect points to the saved URL. 'get()' looks up the key '==' checks if the value matches what was expected

def test_shorten_duplicate_link():
    #Arrange:swap the real Redis for the dummy
    fake_r = fakeredis.FakeRedis(decode_responses=True)# make the dummy
    app_module.r = fake_r                              # app now uses the dummy 
    fake_r.set("url:https://youtube.com", "byftRw")    # reverse key: long URL → existing code (makes it a duplicate)
    client = app.test_client()                         # the fake browser
    # Act: visit the url: like a browser would - > "https://youtube.com"
    response = client.post("/shorten", data={"url": "https://youtube.com"})# same URL as the reverse key, so it's a duplicate
    # Assert: check what came out 
    text = response.text.strip()# the reply, minus the trailing \n
    assert response.status_code == 200# 200 = OK (plain text, not a redirect)
    assert text == "Link already in use. Use code: byftRw" # app hands back the EXISTING code, not a new one

def test_redirect_unknown_code():
     #Arrange:swap the real Redis for the dummy
    fake_r = fakeredis.FakeRedis(decode_responses=True)
    app_module.r = fake_r
    fake_r.set("EK0ZaQ", "https://spotify.com")# save an actual short and long url.
    client = app.test_client()    
    # Act: visit a different short link than what is set for fakeredis
    response = client.get("/qRNGdA")# intentionally send the client to different short url
    # Assert: check what came out  
    assert response.status_code == 404# wrong url shows a "404 not found"
    







    
    
        
