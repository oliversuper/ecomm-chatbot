import openai
import json
from difflib import get_close_matches

# Set up OpenAI API Key
openai.api_key = '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'

# Mock product catalog (replace with real data from a database or API)
product_catalog = {
    "jackets": ["Winter Coat", "Leather Jacket", "Rain Jacket"],
    "sneakers": ["Running Shoes", "High Tops", "Casual Sneakers"],
    "gloves": ["Wool Gloves", "Leather Gloves", "Thermal Gloves"]
}

# Mock FAQs (replace with real FAQ data from the store)
faq_data = {
    "What is your return policy?": "You can return items within 30 days of purchase for a full refund.",
    "What are your shipping options?": "We offer standard, expedited, and next-day shipping.",
    "Where is my order?": "Please provide your order number to track your order."
}

# Fuzzy matching function for better typo handling
def fuzzy_match(input_text, options):
    matches = get_close_matches(input_text.lower(), [option.lower() for option in options], n=1, cutoff=0.7)
    return matches[0] if matches else None

# Function to handle FAQ responses
def handle_faq(user_question):
    matched_faq = fuzzy_match(user_question, faq_data.keys())
    if matched_faq:  # If a close match is found, fetch the associated response
        return faq_data[matched_faq]
    return "I'm sorry, I couldn't find an answer to your question. Can you rephrase it?"

# Function to handle product recommendations
def recommend_products(user_input):
    matched_category = fuzzy_match(user_input, product_catalog.keys())
    if matched_category:  # If a close match is found, fetch the associated recommendations
        recommendations = product_catalog[matched_category]
        return f"Here are some recommendations for {matched_category}: {', '.join(recommendations)}."
    return "I couldn't find any recommendations for that category."

# Main chatbot function
def chatbot_response(user_input):
    print("Debug: Entered chatbot_response")
    print(f"User input: {user_input}")

    # First, check if it's a FAQ question
    faq_response = handle_faq(user_input)
    if faq_response != "I'm sorry, I couldn't find an answer to your question. Can you rephrase it?":
        return faq_response

    # Check for product recommendations
    if "recommend" in user_input.lower():
        return recommend_products(user_input)

    # Default to AI-generated response for other queries
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant for an e-commerce store."},
                {"role": "user", "content": user_input}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Sorry, there was an error: {str(e)}"

# Flask integration for web app deployment
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    response = chatbot_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
