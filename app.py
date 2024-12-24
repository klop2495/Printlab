import os
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError(
        "OPENAI_API_KEY environment variable is not set. "
        "Please set it in your environment."
    )

# ... (other routes like /, /test-key, /get-openai-version) ...

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # This is the simplified code for testing:
        return jsonify({'message': 'OpenAI library accessible'}), 200 
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=False)
