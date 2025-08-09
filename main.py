from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

# Configure CORS - choose one of these options:

# OPTION 1: Allow all origins (for development)
# CORS(app)

# OPTION 2: Allow specific origins (recommended for production)
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://127.0.0.1:5500",  # Your local development
            "https://your-frontend-domain.com",  # Your production frontend
            "https://*.railway.app"  # Allow all Railway domains
        ],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

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
        
        # Return the response with CORS headers
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

@app.after_request
def after_request(response):
    # Add additional headers if needed
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
