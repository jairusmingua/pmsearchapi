from django.db import models


class Song(models.Model):
    class SongSource(models.TextChoices):
        SPOTIFY = 'SPOTIFY'
        YT = 'YT'

    song_id: int = models.AutoField(
        verbose_name='Song ID',
        help_text='Internal ID for private reference',
        primary_key=True
    )
    title = models.CharField(
        max_length=255,
    )
    isrc = models.CharField(
        max_length=255
    )
    source = models.CharField(
        max_length=10,
        choices=SongSource.choices
    )
    artist = models.CharField(
        max_length=255
    )
    external_id = models.CharField(
        max_length=255,
        unique=True
    )
    thumbnail_src = models.CharField(
        max_length=255
    )
    class Meta:
        db_table = 'pm_song'
        ordering = ['song_id']

    def __str__(self):
        return f'[{self.source}] {self.title} - {self.artist}'

    def __repr__(self):
        return f'[{self.source}] {self.title} - {self.artist}'

