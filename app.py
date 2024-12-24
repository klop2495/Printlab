import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/test-key', methods=['GET'])
def test_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return jsonify({'error': 'OPENAI_API_KEY is not set'}), 500
    return jsonify({'message': 'OPENAI_API_KEY is set correctly', 'key': api_key[:5] + '***'}), 200

if __name__ == '__main__':
    app.run()
