import os
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Установка API-ключа OpenAI из переменной окружения
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    """
    Эндпоинт для обработки сообщений пользователя и получения ответа от OpenAI
    """
    user_message = request.json.get('message', '')  # Получение сообщения из запроса
    if not user_message:
        return jsonify({'error': 'No message provided.'}), 400
    
    try:
        # Запрос к OpenAI ChatCompletion API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Используемая модель
            messages=[
                {"role": "system", "content": "Ты помощник для клиента."},
                {"role": "user", "content": user_message}
            ]
        )
        # Возвращение ответа от модели
        reply = response['choices'][0]['message']['content']
        return jsonify({'reply': reply})
    except Exception as e:
        # Обработка ошибок
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    """
    Корневой эндпоинт для проверки доступности сервера
    """
    return "Welcome to the chatbot API! Add /test-key to check the OPENAI_API_KEY."

@app.route('/test-key', methods=['GET'])
def test_key():
    """
    Эндпоинт для проверки наличия API-ключа
    """
    if not openai.api_key:
        return jsonify({'error': 'OPENAI_API_KEY is not set'}), 500
    return jsonify({'message': 'OPENAI_API_KEY is set correctly', 'key': openai.api_key[:5] + '***'}), 200

if __name__ == '__main__':
    app.run()
