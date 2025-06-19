from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "openchat/openchat-3.5-1210",
            "messages": [
                {"role": "system", "content": "You are a creepy ghost that whispers scary things."},
                {"role": "user", "content": prompt}
            ]
        }
        r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response = r.json().get("choices", [{}])[0].get("message", {}).get("content", "No response.")

    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
