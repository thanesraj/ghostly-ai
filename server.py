from flask import Flask, request, render_template
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form.get("prompt")

        try:
            if not OPENROUTER_API_KEY:
                return "👻 API key missing. Check your .env file."

            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {"role": "system", "content": "You are a creepy ghost. Reply eerily, whisper when needed, and include creepy words like *giggle*, *whispers*, *pauses*, and *chuckles*."},
                    {"role": "user", "content": prompt}
                ]
            }

            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            print("RESPONSE STATUS:", response.status_code)
            print("RESPONSE BODY:", response.text)

            if response.status_code == 200:
                result = response.json()
                reply = result["choices"][0]["message"]["content"]
                return reply
            else:
                return f"👻 Error from API: {response.status_code} – {response.text}"

        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"👻 Server Error: {str(e)}"

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
