# music/models.py

from django.conf import settings
from django.db import models


class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    school = models.CharField(max_length=255, default="未知流派")

    def __str__(self):
        return f"{self.title} by {self.artist}"


class SongLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="liked_songs"
    )
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "song")
        db_table = "song_likes"
