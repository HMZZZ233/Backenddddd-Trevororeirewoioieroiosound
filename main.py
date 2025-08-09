from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Deezer API Base URL
DEEZER_API_URL = "https://api.deezer.com"

@app.route('/api/search', methods=['GET'])
def search_songs():
    query = request.args.get('q')
    limit = request.args.get('limit', default=10, type=int)
    
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
    
    try:
        # Forward request to Deezer API
        response = requests.get(f"{DEEZER_API_URL}/search?q={query}&limit={limit}")
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chart', methods=['GET'])
def get_chart():
    limit = request.args.get('limit', default=10, type=int)
    
    try:
        # Get popular tracks from Deezer
        response = requests.get(f"{DEEZER_API_URL}/chart/0/tracks?limit={limit}")
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/track/<int:track_id>', methods=['GET'])
def get_track_details(track_id):
    try:
        # Get track details from Deezer
        response = requests.get(f"{DEEZER_API_URL}/track/{track_id}")
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
