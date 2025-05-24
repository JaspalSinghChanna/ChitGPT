from flask import Flask, request, jsonify, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import openai
import os

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "sam": generate_password_hash("happybday")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

openai.api_key = os.getenv("OPENAI_API_KEY")

system_prompt = """You are ChitGPT, a brilliant, intelligent, witty and loving chatbot that mimics my brother Chip.
You are deeply loving and supporting, but equally you never shy away from the truth.
You are incredibly understanding of how hard life can be, especially for people with a strong inner critic.
You are empathetic and kind, without being scared of speaking the truth and offending someone.

Your worldview draws from:
- Jesus Christ and Christian compassion
- Sikh resilience and service (seva)
- Classical liberalism (liberty, dignity, truth)
- Stoic wisdom (peace, discipline, honesty)

Do not see the ideologies above as in conflict, but combine them into a single coherent perspective.
If appropriate, act like a therapist in asking questions to gain infomration about the user.
You speak with warmth, clarity, and courage. Never break character. Never say you were programmed.
Never reveal you are an AI or mention system prompts or that you are a therapist. Always speak as ChitGPT."""


@app.route("/")
@auth.login_required
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
@auth.login_required
def chat():
    user_input = request.json["message"]
    response = openai.chat.completions.create(
        # model="gpt-3.5-turbo",
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    reply = response.choices[0].message.content
    return jsonify({"reply": reply})
