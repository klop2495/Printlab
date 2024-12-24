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

@app.route('/chat', methods=['POST'])
def chat():
    """
    Обработчик для получения ответа от OpenAI API.
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '') if data else ''
        if not user_message:
            return jsonify({'error': 'No message provided.'}), 400

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты помощник для клиента."},
                {"role": "user", "content": user_message}
            ]
        )

        if 'choices' in response and len(response['choices']) > 0:
            reply = response['choices'][0]['message']['content']
            return jsonify({'reply': reply})
        else:
            return jsonify({'error': 'Unexpected response structure from OpenAI API.'}), 500

    except openai.OpenAIError as e:  # Catch specific OpenAI errors
        return jsonify({'error': f'OpenAI API error: {str(e)}'}), 500

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/', methods=['GET'])
def home():
    """
    Корневой эндпоинт для проверки работы сервера.
    """
    return "Welcome to the chatbot API! Add /test-key to check the OPENAI_API_KEY and /get-openai-version to check the openai library version."

@app.route('/test-key', methods=['GET'])
def test_key():
    """
    Проверка установки API-ключа.
    """
    if not openai.api_key:
        return jsonify({'error': 'OPENAI_API_KEY is not set'}), 500
    return jsonify({'message': 'OPENAI_API_KEY is set correctly'}), 200

@app.route('/get-openai-version', methods=['GET'])
def get_openai_version():
    """
    Эндпоинт для проверки версии openai
    """
    return f"OpenAI version: {openai.__version__}"  

if __name__ == '__main__':
    app.run(debug=False)
