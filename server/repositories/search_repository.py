import re
import logging
from typing import List, Tuple
from server.services import (
    yt_service, 
    spotify_service
)
from server.models import Song

logger = logging.getLogger(__name__)


def search(source: str, artist: str = None, 
           title: str = None, isrc: str = None, external_id: str = None 
) -> List[Song]:
    prefix = 'search'
    try:
        # -- Cleanups -- #
        # Correct Youtube Source Naming For Videos with Improper Naming
        # Search Youtube API for the external_id and formalize artist and 
        # song title
        if source == Song.SongSource.YT and external_id:
            yt_song : Song
            success, yt_song = yt_service.yt_search(external_id=external_id)
            title = yt_song.title
            # try to remove (feat.)
            title = re.sub(r'\(f.*\)','',title)
            artist = yt_song.artist

        # -- Exceptions -- #
        # Add Exceptions For Song Source Types
        if artist == None and title == None and isrc == None and source == Song.SongSource.SPOTIFY:
            raise Exception('Invalid Params')
        
        if artist == None and title == None and source == Song.SongSource.YT:
            raise Exception('Invalid Params')

        # -- DB Query -- #
        logger.debug(f'{prefix} >> Searching From Database')
        filter_kwargs = {}
        filter_kwargs = {**filter_kwargs, 'isrc': isrc} \
                        if isrc != None else filter_kwargs
        filter_kwargs = {**filter_kwargs, 'artist__icontains': artist, 'title__icontains' : title} \
                        if (artist != None and title != None) else filter_kwargs

        result = Song.objects.filter(**filter_kwargs).exclude(source=source)
        if result:
            return True, result

        # -- API Layers -- #
        logger.debug(f'{prefix} >> Searching From APIs')
        api_results: List[Song] = []

        # Spotify Layer
        success, spotify_song = spotify_search(source, artist, title, isrc, external_id)
        if not success:
            logging.error(f'{prefix} >> {spotify_song}')
        else:
            api_results.append(spotify_song)

        # Youtube Layer
        success, yt_song = yt_search(source, spotify_song.artist,\
                                     spotify_song.title, spotify_song.isrc, \
                                     external_id)
        if not success:
            logging.error(f'{prefix} >> {yt_song}')
        else:
            api_results.append(yt_song)

        api_results = [song for song in api_results if song.source != source]

        return True, api_results
    except Exception as error:
        logging.error(f'{prefix} >> {error}')
        return False, []


def yt_search(source: str, artist: str = None, 
              title: str = None, isrc: str = None, external_id: str = None
) -> Tuple[bool , Song]:
    prefix = 'yt_search'
    try:
        # external_id - available
        # isrc - not available
        success, song = yt_service.yt_search(artist=artist,\
                                             title=title)
        if not success:
            logging.error(f'{prefix} >> {song}')
            return False, None

        yt_song, _ = Song.objects.get_or_create(**{
            'title': title if title else song.title,
            'artist': artist if artist else song.artist,
            'external_id': song.external_id,
            'thumbnail_src': song.thumbnail_src,
            'isrc': isrc,
            'source': Song.SongSource.YT.value
        })
        return True, yt_song
    except Exception as error:
        logger.error(f'{prefix} >> {error}')
        return False, None


def spotify_search(source: str, artist: str = None, 
              title: str = None, isrc: str = None, external_id: str = None
) -> Tuple[bool , Song]:
    prefix = 'spotify_search'
    try:
        # external_id - available
        # isrc - available
        if isrc:
            success, song = spotify_service.spotify_search(isrc=isrc)
            if not success:
                success, song = spotify_service.spotify_search(artist=artist,\
                                                            title=title)
        else:
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
        return True, spotify_song
    except Exception as error:
        logger.error(f'{prefix} >> {error}')
        return False, None