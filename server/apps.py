from django.apps import AppConfig


class ServerConfig(AppConfig):
    name = 'server'

    def ready(self):
        from server.services import yt_service
        from server.services import spotify_service
        yt_service.setup(None)
        spotify_service.setup(None)
