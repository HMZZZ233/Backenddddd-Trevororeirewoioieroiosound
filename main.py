from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

GENIUS_API_TOKEN = 'Xdvmlh4Du_NUYKundutVXAaeS2sre59XYY-qcyFg6pBF96NafK6riyVxyRYLg5U9P9E2zCN0eQNa7XeWVVjvKA'

def search_song_lyrics_url(query):
    url = "https://api.genius.com/search"
    headers = {'Authorization': f'Bearer {GENIUS_API_TOKEN}'}
    params = {'q': query}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return None

    data = response.json()
    hits = data['response']['hits']
    if not hits:
        return None

    # Ambil lagu pertama dari hasil search
    song_info = hits[0]['result']
    return song_info['url']  # URL halaman lirik Genius

def scrape_lyrics(genius_url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    page = requests.get(genius_url, headers=headers)
    if page.status_code != 200:
        return None

    soup = BeautifulSoup(page.text, 'html.parser')
    
    # Genius mengemas lirik di tag <div> dengan atribut data-lyrics-container="true"
    lyrics_divs = soup.find_all("div", attrs={"data-lyrics-container": "true"})
    if not lyrics_divs:
        return None

    lyrics = "\n".join(div.get_text(separator="\n").strip() for div in lyrics_divs)
    return lyrics.strip()

@app.route('/lyrics')
def get_lyrics():
    title = request.args.get('title')
    artist = request.args.get('artist')

    if not title or not artist:
        return jsonify({"error": "Parameter title dan artist wajib"}), 400

    query = f"{title} {artist}"
    genius_url = search_song_lyrics_url(query)
    if not genius_url:
        return jsonify({"error": "Lagu tidak ditemukan"}), 404

    lyrics = scrape_lyrics(genius_url)
    if not lyrics:
        return jsonify({"error": "Lirik tidak ditemukan"}), 404

    return jsonify({"lyrics": lyrics})

if __name__ == '__main__':
    app.run(debug=True)
