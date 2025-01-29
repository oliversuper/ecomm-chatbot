from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

ORDERS_FILE = "orders.json"

# Function to load orders from JSON file
def load_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}  # Return empty dictionary if file is empty or corrupted
    return {}

# Function to save orders to JSON file
def save_orders(orders):
    with open(ORDERS_FILE, "w") as file:
        json.dump(orders, file, indent=4)  # Saves the file in a readable format

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").lower()
    orders = load_orders()  # Load existing orders

    # Basic greeting
    if "hello" in message or "hi" in message:
        return jsonify({"response": "Hey there! How can I help?"})

    # Product recommendation
    if "recommend something" in message:
        return jsonify({"response": "I recommend Sony Headphones"})

    if "recommend shoes" in message:
        return jsonify({"response": "I recommend Nike Air Force 1!"})

    if "recommend electronics" in message:
        return jsonify({"response": "I recommend Apple AirPods!"})

    if "recommend clothing" in message:
        return jsonify({"response": "I recommend a Nike T-Shirt!"})

    # Placing an order
    if "place order" in message:
        new_order_id = f"{len(orders) + 1:05d}"  # Generate new order ID (e.g., 00001)
        orders[new_order_id] = "Out for Delivery"
        save_orders(orders)
        return jsonify({"response": f"Your order has been placed! Your order number is {new_order_id}."})

    # Checking order status
    if "order" in message:
        order_id = message.replace("order ", "").strip()
        if order_id in orders:
            return jsonify({"response": f"Order {order_id} is currently: {orders[order_id]}"})
        return jsonify({"response": "Order not found. Please check your order number."})

    return jsonify({"response": "Sorry, I didn't understand that. Can you please rephrase?"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
