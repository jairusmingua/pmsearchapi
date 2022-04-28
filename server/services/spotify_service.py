import logging
import requests
import base64
import urllib.parse
from server.models import Song

logger = logging.getLogger(__name__)

client_username = 'feee3099407b45cb8e94fe043dd6baf1'
client_password = '952dadc2753f4323910ae5d858affad0'

def spotify_generate_token():
    prefix = 'spotify_generate_token'

    url = 'https://accounts.spotify.com/api/token'
    key = base64.b64encode(f'{client_username}:{client_password}'.encode()).decode('utf-8')
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {key}'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    try:
        logger.debug(f'{prefix} >> Generating Token')
        response = requests.post(url=url, headers=headers, data=data)
        response_json = response.json()
        access_token = response_json.get('access_token')
        return True, access_token
    except Exception as error:
        logger.error(f'{prefix} >> {error}')
        return False, None 

def spotify_search(isrc: str = None, artist: str = None, title: str = None):
    prefix = 'spotify_search'
    # NOTE : Not sure if we'll clean artist and title that are hard to search
    # artist = artist.replace('\'','') #clean titles like Boo'd to Bood
    # title = title.replace('\'','') #clean titles like Boo'd to Bood
    isrc = isrc.upper() if isrc else None
    query = f'artist:{artist} track:{title}'
    if isrc:
        query = f'isrc:{isrc}'

    _, token = spotify_generate_token()
    url = f'https://api.spotify.com/v1/search?query={query}&type=track&include_external=audio&offset=0&limit=20'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    try:
        logger.debug(f'{prefix} >> Calling Spotify Search API')
        response = requests.get(url=url, headers=headers)
        song = response.json()

        if len(song['tracks']['items']) == 0:
            return False, 'Song Not Found in SPOTIFY'

        return True, Song(**{
            'title': song['tracks']['items'][0]['name'],
            'artist': song['tracks']['items'][0]['artists'][0]['name'],
            'external_id': song['tracks']['items'][0]['id'],
            'thumbnail_src': song['tracks']['items'][0]['album']['images'][0]['url'],
            'isrc': song['tracks']['items'][0]['external_ids']['isrc'],
            'source': 'SPOTIFY'
        })
    except Exception as error:
        logger.error(f'{prefix} >> {error}')
        return False, None


def setup(config):
    pass

