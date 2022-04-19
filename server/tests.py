from django.test import TestCase

from server.services.yt_service import yt_search
from server.services.spotify_service import spotify_search

title = 'Boo\'d Up'
artist = 'Ella Mai'

success, song = yt_search(title=title, artist=artist)
if success:
    print(song.title)
else:
    print('No results in YT')

success, song = spotify_search(title=title, artist=artist)
if success:
    print(song.title)
else:
    print('No results in Spotify')