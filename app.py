from flask import Flask, jsonify, request, send_file
from collections import deque, Counter

app = Flask(__name__)

hist = deque(maxlen=60)
stats = Counter()

def analise():
    if len(hist) < 6:
        return "Dados insuficientes"

    ultimos = list(hist)[:6]
    streak = len(list(iter(lambda: ultimos[0], None)))

    contagem = Counter(ultimos)
    dominante = contagem.most_common(1)[0][0]

    return {
        "dominante_recente": dominante,
        "sequencia": contagem[dominante],
        "nota": "Tendência estatística visual (não é recomendação de aposta)"
    }

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
        "percent": {
            k: round((stats[k]/total)*100,1) if total else 0
            for k in ["PLAYER","BANKER","TIE"]
        },
        "history": list(hist),
        "analysis": analise()
    })

app.run(host="0.0.0.0", port=10000)
