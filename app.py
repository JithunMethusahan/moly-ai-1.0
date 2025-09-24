from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
from openai import OpenAI

app = Flask(__name__)

# Initialize OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",  # Replace with actual key
    default_headers={
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "moly Chatbot"
    }
)

# Dynamic phrases for landing page
dynamic_texts = [
    "Where should we begin?",
    "What's on your mind?",
    "Ask me anything.",
    "Let's start a conversation.",
    "What are we exploring today?",
    "what we have to do today"
]

# Function to talk to AI
def chat_with_model(prompt):
    try:
        response = client.chat.completions.create(
            model="x-ai/grok-4-fast:free",
            messages=[
                {"role": "system", "content": "You are a helpful and intelligent AI assistant named moly."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error: {e}"

# Landing page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        first_message = request.form.get("message")
        return redirect(url_for("chat", first_message=first_message))
    random_text = random.choice(dynamic_texts)
    return render_template("index.html", dynamic_text=random_text)

# Chat page
@app.route("/chat")
def chat():
    first_message = request.args.get("first_message", "")
    return render_template("chat.html", first_message=first_message)

# API for sending messages dynamically
@app.route("/send_message", methods=["POST"])
def send_message():
    user_message = request.json.get("message")
    ai_response = chat_with_model(user_message)
    
    # Preserve newlines in HTML
    formatted_response = ai_response.replace("\n", "<br>")
    
    return jsonify({"response": formatted_response})


if __name__ == "__main__":
    app.run(debug=True)
