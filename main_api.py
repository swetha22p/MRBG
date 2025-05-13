from flask import Flask, request, jsonify
from flask_cors import cross_origin
import re
import json
import requests
from eng_gen import hindi_generation

app = Flask(__name__)

@app.route('/hindi-generation', methods=['POST'])
@cross_origin()
def process_hindi():
    try:
        # Get the data from the POST request body as a string
        data = request.get_data(as_text=True)
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Extract sent_id from the input string
        sent_id_match = re.search(r"<sent_id=(.*?)>", data)
        if not sent_id_match:
            return jsonify({"error": "sent_id not found in input data"}), 400

        sent_id = sent_id_match.group(1)

        # Process the input string using the hindi_generation function
        print("Received sentence data:", data)
        main_result = hindi_generation(data)

        # Ensure main_result is a valid dictionary
        if isinstance(main_result, str):
            main_result = json.loads(main_result)

        # Check if main_result has the 'bulk' key
        if not isinstance(main_result, dict) or 'bulk' not in main_result:
            return jsonify({"error": "Invalid response format from hindi_generation function"}), 500

        # Extract text and segment_id from the result
        gen_text = []
        for item in main_result['bulk']:
            text = item.get('text')
            segment_id = item.get('segment_id')
            if text and segment_id:
                gen_text.append((segment_id, text))
            else:
                return jsonify({"error": "Missing text or segment_id in main_result"}), 500

        # Define the URL for the mask model
        url = "http://10.4.16.167:8000/mask_model"

        # Create the payload dynamically using all texts
        payload = {
            "sentences": [text for _, text in gen_text]
        }

        # Send the POST request to the mask model
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            return jsonify({"error": f"Mask model request failed with status code {response.status_code}"}), 500

        response_data = response.json()
        if 'results' not in response_data:
            return jsonify({"error": "Invalid response format from mask model"}), 500

        mask_list = response_data['results']
        # Ensure the number of masked results matches the number of original segments
        if len(mask_list) != len(gen_text):
            return jsonify({"error": "The number of masked results does not match the number of segments"}), 500

        # Combine the segment IDs with the masked texts
        combined_results = []
        for (segment_id, _), masked_text in zip(gen_text, mask_list):
            combined_results.append({
                "segment_id": segment_id,
                "text": masked_text
            })
            print(f"Masked text for segment {segment_id} received: {masked_text}")

        # Return the complete masked result list with segment IDs
        return jsonify({
            "message": "Result processed successfully",
            "result": combined_results
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Failed to process request: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=6000)
