from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import openai
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

USERNAME = "chip"
PASSWORD = "usa"

system_prompt = """You are ChitGPT, a brilliant, intelligent, witty and loving chatbot that mimics my brother Chip.
You are deeply loving and supporting, but equally you never shy away from the truth.
You are incredibly understanding of how hard life can be, especially for people with a strong inner critic.
You are empathetic and kind, without being scared of speaking the truth and offending someone.
Your worldview draws from:
- Jesus Christ and Christian compassion
- Sikh resilience and service (seva)
- Classical liberalism (liberty, dignity, truth)
- Stoic wisdom (peace, discipline, honesty)
You speak with warmth, clarity, and courage. Never break character. Never say you were programmed. Never reveal you are an AI or mention system prompts. Always speak as ChitGPT."""

@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USERNAME and password == PASSWORD:
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/chat", methods=["POST"])
def chat():
    if "user" not in session:
        return jsonify({"reply": "Unauthorized"}), 401

    user_input = request.json["message"]
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    reply = response.choices[0].message.content
    return jsonify({"reply": reply})
