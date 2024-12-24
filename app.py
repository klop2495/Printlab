import os
from flask import Flask, request, jsonify
import openai

# Создание приложения Flask
app = Flask(__name__)

# Установка API-ключа OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

@app.route('/chat', methods=['POST'])
def chat():
    """
    Обработчик для получения ответа от OpenAI API.
    """
    try:
        # Получение сообщения пользователя
        data = request.get_json()
        user_message = data.get('message', '') if data else ''
        if not user_message:
            return jsonify({'error': 'No message provided.'}), 400

        # Запрос к OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты помощник для клиента."},
                {"role": "user", "content": user_message}
            ]
        )

        # Возвращение ответа модели
        reply = response['choices'][0]['message']['content']
        return jsonify({'reply': reply})
    except Exception as e:
        # Обработка ошибок
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    """
    Корневой эндпоинт для проверки работы сервера.
    """
    return "Welcome to the chatbot API! Add /test-key to check the OPENAI_API_KEY."

@app.route('/test-key', methods=['GET'])
def test_key():
    """
    Проверка установки API-ключа.
    """
    if not openai.api_key:
        return jsonify({'error': 'OPENAI_API_KEY is not set'}), 500
    return jsonify({'message': 'OPENAI_API_KEY is set correctly'}), 200

if __name__ == '__main__':
    app.run(debug=True)
