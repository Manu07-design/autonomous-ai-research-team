from flask import Flask, request, jsonify
from orchestrator import run_system
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Autonomous AI Research Team Running 🚀"

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    q = data.get("query")

    answer = run_system(q)

    return jsonify({
        "answer": answer
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)