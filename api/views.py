from cmath import log
import logging

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from server.repositories.search_repository import search
from api.serializers import SongSerializer

logger = logging.getLogger(__name__)

@api_view(['GET'])
def search_view(request: Request):
    prefix = 'search_view'
    logger.debug(f'{prefix} >> Generating Search')
    artist = request.query_params.get('artist')
    title = request.query_params.get('title')
    isrc = request.query_params.get('isrc')
    source = request.query_params.get('source')
    
    success, song = search(source=source, artist=artist, title=title, isrc=isrc)
    if not success:
        logger.error(f'{prefix} >> {song}')
        data = {
            'status': 'ERROR',
            'message': 'Song not Found'
        }
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    
    result_data = SongSerializer(instance=song)
    data = {
        'status': 'SUCCESS',
        'result': result_data.data
    }
    return Response(data=data, status=status.HTTP_200_OK)
