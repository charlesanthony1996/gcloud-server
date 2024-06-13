import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from dotenv import load_dotenv
import openai
import requests

# Load environment variables
load_dotenv()
# test line to check for gcloud run health

# Setup Flask application
app = Flask(__name__)
app.debug = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# OpenAI API Key
open_api_key = os.getenv('OPEN_API_KEY')
client = openai.Client(api_key=open_api_key)

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "This is the data from Flask."})

@app.route('/api/comments', methods=['GET'])
def get_comments():
    return jsonify({"comment": "first comment"})

@app.route("/extension/default", methods=["GET"])
def get_default_extension():
    return jsonify({"prompt": "Highlighted"})

@app.route("/api/analyze_hate_speech", methods=["POST"])
def analyze_hate_speech():
    try:
        data = request.get_json()
        comment_text = data.get('text', '')  
        response_comment = comment_text if comment_text else "No comment received"

        responseFromLLM = requests.post("http://openai_backend:6001/api/analyze_hate_speech", json={"text": response_comment})
        analysis_result = responseFromLLM.json().get('analysis_result', '')
        return jsonify({"analysis_result": analysis_result})

    except Exception as e:
        print("Error during processing comments:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route("/api/generate_counter_speech", methods=["POST"])
def generate_counter_speech():
    try:
        data = request.get_json()
        comment_text = data.get('text', '')  
        response_comment = comment_text if comment_text else "No comment received"

        responseFromLLM = requests.post("http://openai_backend:6001/api/generate_counter_speech", json={"text": response_comment})
        counter_speech_result = responseFromLLM.json().get('counter_speech_result', '')
        return jsonify({"counter_speech_result": counter_speech_result})

    except Exception as e:
        print("Error during processing comments:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route("/api/explain_comment", methods=["POST"])
def explain_comment():
    try:
        data = request.get_json()
        comment_text = data.get('text', '')  
        response_comment = comment_text if comment_text else "No comment received"

        explanationFromLLM = requests.post("http://openai_backend:6001/api/explain_hate_speech", json={"text": response_comment})
        explanation_result = explanationFromLLM.json().get('explanation_result', '')
        return jsonify({"explanation_text": explanation_result})

    except Exception as e:
        print("Error during processing comments:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/api/process_comments', methods=['POST'])
def process_comments():
    try:
        data = request.get_json()
        comment_text = data.get('comment', '')  
        response_comment = comment_text if comment_text else "No comment received"
        
        filter_response = requests.post('http://filter:7001/api/test', json={'text': response_comment})
        response = filter_response.json().get('filtered_text')
        if response != "Is not HS":
            filter_responseLLM = requests.post('http://openai_backend:6001/api/analyze_hate_speech', json={'text': response})
            if filter_responseLLM.status_code == 200:
                response = filter_responseLLM.json().get('llm_result')
                return jsonify({"comment": response}), 200
        else:
            return jsonify({"comment": "Is not HS" }), 200
        
    except Exception as e:
        print("Error during processing comments:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
