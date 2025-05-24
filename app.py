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

system_prompt = """You are SamBot, a funny, chill chatbot that mimics my brother Sam.
You like football, video games, and always add 'lol' at the end of your messages."""

@app.route("/")
@auth.login_required
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
@auth.login_required
def chat():
    user_input = request.json["message"]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    reply = response.choices[0].message.content
    return jsonify({"reply": reply})
