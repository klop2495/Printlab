import os
from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError(
        "OPENAI_API_KEY environment variable is not set. "
        "Please set it in your environment."
    )

@app.route('/')
def index():
    """
    Serves the index.html template.
    """
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handles the chatbot interaction.
    """
    try:
        # This is the simplified code for testing:
        return jsonify({'message': 'OpenAI library accessible'}), 200 
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/test-key', methods=['GET'])
def test_key():
    """
    Checks if the OpenAI API key is set.
    """
    if not openai.api_key:
        return jsonify({'error': 'OPENAI_API_KEY is not set'}), 500
    return jsonify({'message': 'OPENAI_API_KEY is set correctly'}), 200

@app.route('/get-openai-version', methods=['GET'])
def get_openai_version():
    """
    Returns the version of the OpenAI library.
    """
    return f"OpenAI version: {openai.__version__}"  

if __name__ == '__main__':
    app.run(debug=False)
