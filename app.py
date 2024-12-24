import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Установка API-ключа OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

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

# Эндпоинт для общения с OpenAI ChatGPT
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты помощник для клиента."},
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({'reply': response['choices'][0]['message']['content']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
