import os
import anthropic  # Ensure this is in requirements.txt
from flask import Flask, request, jsonify

app = Flask(__name__)

# Anthropic API Key (Claude AI)
ANTHROPIC_API_KEY = "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"

# Initialize Anthropic Client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

@app.route("/")
def home():
    return "E-Commerce Chatbot is Running!"

@app.route("/chat", methods=["POST"])
def chat():
    """Handles chatbot messages."""
    user_input = request.json.get("message", "")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = client.messages.create(
            model="claude-2.1",
            max_tokens=200,
            messages=[{"role": "user", "content": user_input}]
        )

        # Extract the AI response
        reply = response.content[0].text if response.content else "Sorry, I couldn't generate a response."

        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
