import os
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Настройка API-ключа OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided.'}), 400
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Замените на "gpt-3.5-turbo", если GPT-4 недоступен в вашем тарифе
            messages=[
                {"role": "system", "content": "Ты помощник для клиента."},
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({'reply': response['choices'][0]['message']['content']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the chatbot API! Add /test-key to check the OPENAI_API_KEY."

@app.route('/test-key', methods=['GET'])
def test_key():
    if not openai.api_key:
        return jsonify({'error': 'OPENAI_API_KEY is not set.'}), 500
    return jsonify({'message': 'OPENAI_API_KEY is set correctly', 'key': openai.api_key[:5] + '***'}), 200

if __name__ == '__main__':
    app.run()
