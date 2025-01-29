from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
ORDERS_FILE = "orders.json"

def load_orders():
    """Loads existing orders from the JSON file."""
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}  # Return empty dict if file is corrupted
    return {}

def save_orders(orders):
    """Saves orders to the JSON file."""
    with open(ORDERS_FILE, "w") as file:
        json.dump(orders, file, indent=4)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip().lower()
    
    orders = load_orders()  # Load orders from file
    
    if message == "place order":
        new_order_id = str(len(orders) + 1).zfill(5)  # Generate order ID like "00001"
        orders[new_order_id] = "Out for Delivery"
        save_orders(orders)  # Save updated orders
        return jsonify({"response": f"Your order has been placed! Your order number is {new_order_id}."})
    
    elif message.startswith("order"):
        order_id = message.split(" ")[-1].zfill(5)  # Extract order number
        if order_id in orders:
            return jsonify({"response": f"Order {order_id} is currently: {orders[order_id]}"})
        else:
            return jsonify({"response": "Order not found. Please check your order number."})

    # Fix recommendation feature
    elif "recommend" in message:
        if "shoes" in message:
            return jsonify({"response": "I recommend Nike Air Force 1!"})
        elif "electronics" in message:
            return jsonify({"response": "I recommend Apple AirPods!"})
        elif "clothing" in message:
            return jsonify({"response": "I recommend a Nike T-Shirt!"})
        else:
            return jsonify({"response": "I recommend Sony Headphones!"})  # Default recommendation

    # Greeting
    elif "hello" in message or "hi" in message:
        return jsonify({"response": "Hey there! How can I help?"})
    
    return jsonify({"response": "Invalid request."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
