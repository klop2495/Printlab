import os
from flask import Flask, jsonify

app = Flask(__name__)

# Эндпоинт для проверки OPENAI_API_KEY
@app.route('/test-key', methods=['GET'])
def test_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return jsonify({'error': 'OPENAI_API_KEY is not set'}), 500
    return jsonify({'message': 'OPENAI_API_KEY is set correctly', 'key': api_key[:5] + '***'}), 200

# Эндпоинт для корневого URL
@app.route('/', methods=['GET'])
def home():
    return "Welcome to the chatbot API! Add /test-key to check the OPENAI_API_KEY."

if __name__ == '__main__':
    app.run()
