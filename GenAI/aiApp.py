# aiApp.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from GenAI import LLM_connect

# 1) Create app and enable CORS on all routes
app = Flask(__name__)
CORS(app)  # applies to every route by default :contentReference[oaicite:5]{index=5}

# 2) Initialize your LLM client once
llm = LLM_connect()

@app.route('/')
def root():
    return 'Gen API connected'

@app.route('/ai/test/<question>')
def test_chat(question):
    answer = llm.chat(question)
    return jsonify({'answer': answer})

@app.route('/ai/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'status': 400, 'error': 'Missing "question" in request body'}), 400

    try:
        answer = llm.chat(question)
        return jsonify({'status': 200, 'answer': answer})
    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
