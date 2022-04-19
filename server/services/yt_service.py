import logging
from ytmusicapi import YTMusic
from server.models import Song


def yt_search(title: str, artist: str):
    prefix = 'yt_search'
    try:
        ytmusicapi = YTMusic()
        response = ytmusicapi.search(f'{title} - {artist}')
        for result in response:
            if result['category'] == 'Songs':
                return True, Song(**{
                    'title': result['title'],
                    'artist': result['artists'][0]['name'],
                    'thumbnail_src': result['thumbnails'][1]['url'],
                    'external_id': result['videoId'],
                    'source': 'YT'
                })
        return False, 'Song Not Found in YT'
                
    except Exception as error:
        return False, None

def setup(config):
    pass