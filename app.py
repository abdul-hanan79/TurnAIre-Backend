from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Create this HTML file for input/output.

@app.route('/chat', methods=['POST'])
def chat():
    user_query = request.form.get('query')
    if not user_query:
        return jsonify({"error": "Query cannot be empty"}), 400

    # Call FastAPI backend
    try:
        response = requests.post(
            "http://localhost:8000/api/chat",
            json={"query": user_query},
        )
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
