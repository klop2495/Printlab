@app.route('/chat', methods=['POST'])
def chat():
    try:
        return jsonify({'message': 'OpenAI library accessible'}), 200
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
