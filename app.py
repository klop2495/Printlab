	import os
from flask import Flask, request, jsonify
import openai
 
# Create Flask application
app = Flask(__name__)
 
# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
 
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")
 
@app.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint for processing user messages and getting a response from OpenAI
    """
    try:
        # Get message from request body
        data = request.get_json()
        user_message = data.get('message', '') if data else ''
        if not user_message:
            return jsonify({'error': 'No message provided.'}), 400
 
        # Send request to OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        # Extract response from model
        reply = response['choices'][0]['message']['content']
        return jsonify({'reply': reply})
    except openai.error.OpenAIError as e:
        # Handle OpenAI API errors
        return jsonify({'error': f'OpenAI API error: {str(e)}'}), 500
    except Exception as e:
        # General error handling
        return jsonify({'error': f'Server error: {str(e)}'}), 500
 
@app.route('/', methods=['GET'])
def home():
    """
    Root endpoint for checking server status
    """
    return "Welcome to the chatbot API! Add /test-key to check the OPENAI_API_KEY."
 
@app.route('/test-key', methods=['GET'])
def test_key():
    """
    Endpoint to check the presence of the API key
    """
    if not openai.api_key:
        return jsonify({'error': 'OPENAI_API_KEY is not set'}), 500
    return jsonify({'message': 'OPENAI_API_KEY is set correctly'}), 200
 
if __name__ == '__main__':
    app.run(debug=True)
