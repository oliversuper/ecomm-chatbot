import os
from flask import Flask, request, jsonify
import anthropic  # Claude AI integration

app = Flask(__name__)

# AI API Key
ANTHROPIC_API_KEY = "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"
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

@app.route("/")
def home():
    return "E-Commerce Chatbot is Running!"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # Send user message to AI
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=300,
            messages=[{"role": "user", "content": user_message}]
        )

        return jsonify({"response": response.content[0].text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Corrected Port Binding for Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
