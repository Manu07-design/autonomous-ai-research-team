from flask import Flask, request, jsonify
from flask_cors import CORS
from orchestrator import run_system
import os

app = Flask(__name__)
CORS(app)

# ---------------- CHATGPT-STYLE UI ----------------
@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>AI Research Copilot</title>
        <style>
            body {
                font-family: Arial;
                background: #0f172a;
                color: white;
                margin: 0;
            }

            #chat {
                height: 85vh;
                overflow-y: auto;
                padding: 20px;
            }

            .user {
                text-align: right;
                margin: 10px;
            }

            .bot {
                text-align: left;
                margin: 10px;
            }

            .bubble {
                display: inline-block;
                padding: 10px 15px;
                border-radius: 15px;
                max-width: 60%;
                white-space: pre-wrap;
            }

            .user .bubble {
                background: #2563eb;
            }

            .bot .bubble {
                background: #1e293b;
            }

            #input-area {
                position: fixed;
                bottom: 0;
                width: 100%;
                background: #020617;
                padding: 10px;
                display: flex;
            }

            input {
                flex: 1;
                padding: 10px;
                border-radius: 10px;
                border: none;
                outline: none;
            }

            button {
                margin-left: 10px;
                padding: 10px 20px;
                border-radius: 10px;
                border: none;
                background: #2563eb;
                color: white;
                cursor: pointer;
            }

            button:hover {
                background: #1d4ed8;
            }
        </style>
    </head>

    <body>

        <div id="chat"></div>

        <div id="input-area">
            <input id="query" placeholder="Ask something...">
            <button onclick="send()">Send</button>
        </div>

        <script>
        async function send() {
            let input = document.getElementById("query");
            let chat = document.getElementById("chat");

            let text = input.value;
            if (!text) return;

            // USER MESSAGE
            chat.innerHTML += `
                <div class="user">
                    <div class="bubble">${text}</div>
                </div>
            `;

            input.value = "";

            // BOT LOADING
            let loadingId = "loading-" + Date.now();
            chat.innerHTML += `
                <div class="bot" id="${loadingId}">
                    <div class="bubble">Typing...</div>
                </div>
            `;

            chat.scrollTop = chat.scrollHeight;

            try {
                let res = await fetch("/query", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({query: text})
                });

                let data = await res.json();

                document.getElementById(loadingId).remove();

                // BOT RESPONSE
                chat.innerHTML += `
                    <div class="bot">
                        <div class="bubble">${data.answer}</div>
                    </div>
                `;
            } catch (error) {
                document.getElementById(loadingId).remove();

                chat.innerHTML += `
                    <div class="bot">
                        <div class="bubble"> Error: Unable to fetch response</div>
                    </div>
                `;
            }

            chat.scrollTop = chat.scrollHeight;
        }
        </script>

    </body>
    </html>
    """

# ---------------- API ----------------
@app.route("/query", methods=["POST"])
def query():
    data = request.json
    q = data.get("query")

    if not q:
        return jsonify({"answer": "Please enter a question."})

    answer = run_system(q)

    return jsonify({"answer": answer})


# ---------------- MAIN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)