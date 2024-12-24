import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Получение API-ключа из переменных окружения
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Hello, Printlab!"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided.'}), 400

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
    app.run(debug=True)
