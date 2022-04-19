from rest_framework import serializers

from server.models import Song

class SongSerializer(serializers.Serializer):
    title = serializers.CharField()
    source = serializers.CharField()
    artist = serializers.CharField()
    external_id = serializers.CharField()
    thumbnail_src = serializers.CharField()
 
    def to_representation(self, instance):
        song = instance
        instance = super().to_representation(instance)
        url = song.external_id
        if song.source == Song.SongSource.YT.value:
            url = f'https://music.youtube.com/watch?v={song.external_id}'
            thumbnail_src = song.thumbnail_src
            thumbnail_src = thumbnail_src.replace('w120-h120','w640-h640')
            instance['thumbnail_src'] = thumbnail_src
        elif song.source == Song.SongSource.SPOTIFY.value:
            url = f'https://open.spotify.com/track/{song.external_id}'
        else:
            return instance
        instance['url'] = url
        return instance
    class Meta:
        model = Song
