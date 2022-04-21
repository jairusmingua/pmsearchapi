import logging
from pprint import isrecursive

from server.services import (
    yt_service, 
    spotify_service
)
from server.models import Song

logger = logging.getLogger(__name__)


def search(source: str, artist: str = None, 
           title: str = None, isrc: str = None 
):
    prefix = 'search'
    try:
        filter_source = 'YT' if source == 'SPOTIFY' else 'SPOTIFY'
        logger.debug(f'{prefix} >> Searching From Database')

        if isrc == None:
            result = Song.objects.filter(source=filter_source, artist=artist,\
                                        title=title)\
                                 .first()
        else:
            result = Song.objects.filter(source=filter_source, artist=artist,\
                                        title=title, isrc=isrc)\
                                 .first()
        if result:
            return True, result
        logger.debug(f'{prefix} >> Searching From APIs')
    
        spotify_song: Song
        yt_song: Song
        song : Song

        spotify_song = None
        yt_song = None

        success = None
        if isrc:
            success, song = spotify_service.spotify_search(isrc=isrc)

        if not success:
            success, song = spotify_service.spotify_search(artist=artist,\
                                                        title=title)
        if not success:
            logging.error(f'{prefix} >> {song}')
            return False, None

        spotify_song, _ = Song.objects.get_or_create(**{
            'title': song.title,
            'artist': song.artist,
            'external_id': song.external_id,
            'thumbnail_src': song.thumbnail_src,
            'isrc': song.isrc,
            'source': Song.SongSource.SPOTIFY.value
        })
        
        success, song = yt_service.yt_search(artist=artist,\
                                            title=title)
        if not success:
            logging.error(f'{prefix} >> {song}')
            return False, None

        yt_song, _ = Song.objects.get_or_create(**{
            'title': spotify_song.title,
            'artist': spotify_song.artist,
            'external_id': song.external_id,
            'thumbnail_src': song.thumbnail_src,
            'isrc': spotify_song.isrc,
            'source': Song.SongSource.YT.value
        })

        return True, yt_song if filter_source == 'YT' else spotify_song
    except Exception as error:
        logging.error(f'{prefix} >> {error}')
        return False, None
