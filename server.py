from flask import Flask, render_template, request
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form.get("prompt", "")
        if not prompt:
            return "The ghost is silent..."

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openrouter/ggml-gemma-7b-it",  # You can change model here
            "messages": [
                {"role": "system", "content": "You are a creepy ghost. Answer in a spooky and mysterious tone."},
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            data = response.json()

            ghost_reply = data['choices'][0]['message']['content']
            return ghost_reply
        except Exception as e:
            print("ERROR:", e)
            return "👻 The ghost encountered an error."

    return render_template("index.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
