# playlist/models.py

from django.conf import settings
from django.db import models
from music.models import Song


class Playlist(models.Model):
    name = models.CharField(max_length=255, help_text="歌单名称")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="playlists",
        help_text="创建该歌单的用户",
    )
    songs = models.ManyToManyField(
        Song, related_name="playlists", help_text="歌单中包含的歌曲"
    )

    created_at = models.DateTimeField(auto_now_add=True, help_text="创建时间")
    updated_at = models.DateTimeField(auto_now=True, help_text="更新时间")

    class Meta:
        db_table = "playlists"
        unique_together = (("owner", "name"),)
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} (by {self.owner.username})"
