import logging
from fuzzywuzzy import fuzz
from ytmusicapi import YTMusic
from server.models import Song

logger = logging.getLogger(__name__)

def yt_search(title: str, artist: str):
    prefix = 'yt_search'
    try:
        ytmusicapi = YTMusic()
        response = ytmusicapi.search(f'{title} - {artist}')
        for result in response:
            _title = result['title']
            _artist = result['artists'][0]['name']
            thumbnail_src = result['thumbnails'][0]['url']
            external_id = result['videoId']
            source = 'YT'
            if fuzz.ratio(str(_title).lower(), title.lower()) >= 10 and\
               fuzz.partial_ratio(str(_title).lower(), title.lower()) >= 90 and\
               (result['category'] == 'Top result' or result['category'] == 'Songs'):
                return True, Song(**{
                    'title': _title,
                    'artist': _artist,
                    'thumbnail_src': thumbnail_src,
                    'external_id': external_id,
                    'source': source
                })
        return False, 'Song Not Found in YT'
                
    except Exception as error:
        logger.error(f'{prefix}: {error}')
        return False, None

def setup(config):
    pass