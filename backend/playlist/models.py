# playlist/models.py

from django.conf import settings
from django.db import models
from music.models import Song


class Playlist(models.Model):
    name = models.CharField(max_length=255, help_text="歌单名称")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="playlists",
        help_text="创建该歌单的用户",
    )
    songs = models.ManyToManyField(
        Song, related_name="playlists", help_text="歌单中包含的歌曲"
    )

    def __str__(self):
        return f"{self.name} by {self.user.username}"
