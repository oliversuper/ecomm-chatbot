from flask import Flask, request, jsonify, render_template
import json
import os
import anthropic  # Claude AI integration

app = Flask(__name__)

# Ensure templates folder exists
TEMPLATES_FOLDER = "templates"
if not os.path.exists(TEMPLATES_FOLDER):
    os.makedirs(TEMPLATES_FOLDER)

ORDERS_FILE = "orders.json"

# Claude AI API Key (Replace with your own)
client = anthropic.Anthropic(api_key="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")

# Load orders
def load_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

# Save orders
def save_orders(orders):
    with open(ORDERS_FILE, "w") as file:
        json.dump(orders, file, indent=4)

@app.route("/")
def home():
    return render_template("index.html")

# Function to get response from Claude AI
def get_claude_response(user_message):
    response = client.messages.create(
        model="claude-2",  # Change to "claude-3" if available
        max_tokens=200,
        messages=[{"role": "user", "content": user_message}]
    )
    return response.content

# Chatbot with AI responses
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()

    orders = load_orders()

    # Step 1: Check for specific actions (orders, recommendations)
    if "place order" in message.lower():
        new_order_id = str(len(orders) + 1).zfill(5)
        orders[new_order_id] = "Out for Delivery"
        save_orders(orders)
        return jsonify({"response": f"Your order has been placed! Your order number is {new_order_id}."})

    elif any(keyword in message.lower() for keyword in ["track", "check", "find", "where", "status"]):
        words = message.split()
        for word in words:
            if word.isdigit():  # Check if a number is in the message
                order_id = word.zfill(5)
                if order_id in orders:
                    return jsonify({"response": f"Order {order_id} is currently: {orders[order_id]}"})
        return jsonify({"response": "I couldn't find that order. Can you provide the order number?"})

    elif any(keyword in message.lower() for keyword in ["recommend", "suggest", "buy", "looking for"]):
        return jsonify({"response": "I can help with that! What category? (Shoes, Electronics, Clothing, etc.)"})

    # Step 2: AI-powered conversation using Claude AI
    try:
        ai_response = get_claude_response(message)
        return jsonify({"response": ai_response})
    except Exception as e:
        return jsonify({"response": "I'm having trouble responding right now. Try again later!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
