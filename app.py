from flask import Flask, jsonify, request, send_file
from collections import deque

app = Flask(__name__)
hist = deque(maxlen=40)
stats = {"PLAYER":0,"BANKER":0,"TIE":0}

@app.route("/")
def home():
    return send_file("dashboard.html")

@app.route("/add", methods=["POST"])
def add():
    r = request.json["result"]
    hist.appendleft(r)
    stats[r] += 1
    return jsonify(ok=True)

@app.route("/data")
def data():
    total = sum(stats.values())
    return jsonify({
        "percent": {k: round((v/total)*100,1) if total else 0 for k,v in stats.items()},
        "history": list(hist)
    })

app.run(host="0.0.0.0", port=10000)
