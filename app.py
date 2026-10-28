from flask import Flask, request, redirect, abort
import socket
import os
import redis
import secrets

app = Flask(__name__)
r = redis.Redis(host=os.environ.get("REDIS_HOST","redis"), port=6379, password=os.environ.get("REDIS_PASSWORD"), decode_responses=True)

@app.route("/")
def hello_world():
    name = socket.gethostname()
    return f"localhost:8080/ {name}"

@app.route("/shorten", methods=["POST"])
def shorten():
    long_url = request.form["url"]
    code = secrets.token_urlsafe(4)#randomizes the url to 4 bites > "55vsDQ"
    r.set(code, long_url)
    return f"{code}\n"

@app.route("/<code>")
def go(code):
    long_url = r.get(code)
    if long_url is None:
        abort(404)
    return redirect(long_url)

@app.route("/healthz")
def health_check():
    r.ping()
    return  {"status": "ok", "redis": "connected", "pod": socket.gethostname()}

@app.route("/links")
def stored_links():
    links = {}#empty dict to store old links
    for key in r.scan_iter():#loop through keys: in redis using r.scan_iter, for each code, look up its URL,
        links[key] = r.get(key)#push keys:values from redis to new dict
    
    count = len(links)#length of dict with stored keys
    
    return {
        "message": f"successfully retrieved {count} links",
        "links": links, 
        "links_stored": count
        }#return, best practice is to have all keys: lowercase and no spaces!

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)