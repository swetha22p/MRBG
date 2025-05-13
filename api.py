from flask import Flask, request, jsonify
import json
from eng_gen import hindi_generation  # Replace 'your_module' with the actual module name

app = Flask(__name__)

@app.route('/hindi_generation', methods=['POST'])
def generate_hindi():
    try:
        data = request.get_json()
        input_text = data.get("input_text", "")
        if not input_text:
            return jsonify({"error": "No input text provided"}), 400
        
        output = hindi_generation(input_text)
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)
