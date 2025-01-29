from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# Ensure templates folder exists for rendering HTML
TEMPLATES_FOLDER = "templates"
if not os.path.exists(TEMPLATES_FOLDER):
    os.makedirs(TEMPLATES_FOLDER)

ORDERS_FILE = "orders.json"

# Load existing orders
def load_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}  # Return empty dict if file is corrupted
    return {}

# Save orders to file
def save_orders(orders):
    with open(ORDERS_FILE, "w") as file:
        json.dump(orders, file, indent=4)

# Route for chatbot UI
@app.route("/")
def home():
    return render_template("index.html")

# Chatbot logic
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip().lower()
    
    orders = load_orders()  # Load orders

    # Handle greetings
    if message in ["hi", "hello", "hey"]:
        return jsonify({"response": "Hey there! How can I help?"})

    # Handle small talk
    elif message in ["how are you?", "how's it going?", "what's up?"]:
        return jsonify({"response": "I'm just a bot, but I'm here to help!"})

    # Handle order placement
    elif message == "place order":
        new_order_id = str(len(orders) + 1).zfill(5)  # Generate order ID like "00001"
        orders[new_order_id] = "Out for Delivery"
        save_orders(orders)
        return jsonify({"response": f"Your order has been placed! Your order number is {new_order_id}."})

    # Handle order status
    elif "check my order" in message or message.startswith("order "):
        order_id = message.split(" ")[-1].zfill(5)  # Extract order number
        if order_id in orders:
            return jsonify({"response": f"Order {order_id} is currently: {orders[order_id]}"})
        else:
            return jsonify({"response": "Order not found. Please check your order number."})

    # Handle product recommendations
    elif "recommend" in message or "looking for" in message:
        if "shoes" in message:
            return jsonify({"response": "I recommend Nike Air Force 1!"})
        elif "electronics" in message:
            return jsonify({"response": "I recommend Apple AirPods!"})
        elif "clothing" in message:
            return jsonify({"response": "I recommend a Nike T-Shirt!"})
        else:
            return jsonify({"response": "I recommend Sony Headphones!"})  # Default

    # Catch-all response
    return jsonify({"response": "Sorry, I didn't understand that. Try asking about orders or recommendations!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
