import os
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Установка ключа OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Отправка запроса к OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты помощник для клиента."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response['choices'][0]['message']['content']
        return jsonify({'reply': reply})

    except openai.error.OpenAIError as e:
        print(f"Ошибка OpenAI: {e}")  # Логирование ошибки
        return jsonify({'error': f"OpenAI Error: {str(e)}"}), 500

    except Exception as e:
        print(f"Внутренняя ошибка: {e}")  # Логирование ошибки
        return jsonify({'error': f"Internal Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run()
