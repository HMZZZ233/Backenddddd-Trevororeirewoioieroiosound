import requests

GENIUS_API_TOKEN = 'Xdvmlh4Du_NUYKundutVXAaeS2sre59XYY-qcyFg6pBF96NafK6riyVxyRYLg5U9P9E2zCN0eQNa7XeWVVjvKA'

def search_song_lyrics(query):
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
    song_title = song_info['title']
    artist = song_info['primary_artist']['name']
    url = song_info['url']  # Link Genius halaman lirik

    return {
        'title': song_title,
        'artist': artist,
        'url': url
    }
