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

@app.route('/chat', methods=['POST'])  # This is the updated /chat route
def chat():
    """
    Handles the chatbot interaction.
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '') if data else ''
        if not user_message:
            return jsonify({'error': 'No message provided.'}), 400
        
        response = openai.Completion.create(
            engine="text-davinci-003", 
            prompt=user_message,
            max_tokens=150  
        )
        
        reply = response.choices[0].text.strip()
        return jsonify({'reply': reply})
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
