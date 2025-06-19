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
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": "You are a creepy ghost that whispers in fear."},
                {"role": "user", "content": prompt}
            ]
        }
        try:
            r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
            if r.status_code == 200:
                response = r.json().get("choices", [{}])[0].get("message", {}).get("content", "Ghost didn’t speak.")
            else:
                response = f"Error {r.status_code}: Ghost refused to answer."
        except Exception as e:
            response = f"Exception: {str(e)}"

    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
