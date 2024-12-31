# GitHub Repository Link: https://github.com/idamodhar17/Team-Infinity-SSH-BHU

from flask import Flask, request, jsonify
import joblib
import traceback
import os

app = Flask(__name__)

MODEL_PATH = 'news_classification_model.pkl'
VECTORIZER_PATH = 'tfidf_vectorizer.pkl'

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("Model and vectorizer loaded successfully.")
except Exception as e:
    print("Error loading model or vectorizer:", e)
    model = None
    vectorizer = None

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or vectorizer is None:
        return jsonify({"error": "Model or vectorizer not loaded"}), 500

    try:
        data = request.get_json()
        title = data.get('title', '')
        text = data.get('text', '')

        if not title or not text:
            return jsonify({"error": "Both 'title' and 'text' fields are required"}), 400

        combined_text = title + ' ' + text
        transformed_input = vectorizer.transform([combined_text])

        prediction = model.predict(transformed_input)[0]
        result = "Real" if prediction == 1 else "Fake"

        return jsonify({"prediction": result})

    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the News Classification API!"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
