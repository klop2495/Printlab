import os
from flask import Flask, request, jsonify, render_template
import openai
import json

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError(
        "OPENAI_API_KEY environment variable is not set. "
        "Please set it in your environment."
    )

# Load services data from services.json
with open('services.json', 'r') as f:
    services_data = json.load(f)

services = {service['name']: service for service in services_data['services']}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '') if data else ''
        if not user_message:
            return jsonify({'error': 'No message provided.'}), 400

        if "services" in user_message.lower():  # Check for service-related query
            reply = "Here are our services and prices:\n"
            for service_name, service_details in services.items():
                reply += f"- {service_name}: ${service_details['price']} ({service_details['description']})\n"
            return jsonify({'reply': reply})

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты помощник для клиента."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content
        return jsonify({'reply': reply})
    except openai.OpenAIError as e:
        return jsonify({'error': f'OpenAI API error: {e}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/test-key', methods=['GET'])
def test_key():
    if not openai.api_key:
        return jsonify({'error': 'OPENAI_API_KEY is not set'}), 500
    return jsonify({'message': 'OPENAI_API_KEY is set correctly'}), 200

@app.route('/get-openai-version', methods=['GET'])
def get_openai_version():
    return f"OpenAI version: {openai.__version__}"

if __name__ == '__main__':
    app.run(debug=False)
