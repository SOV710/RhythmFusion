# recommender/models.py

from django.db import models
from music.models import Song


class SongVector(models.Model):
    song = models.OneToOneField(
        Song, on_delete=models.CASCADE, primary_key=True)
    cf_vector = models.JSONField()
    content_vector = models.JSONField()
    hybrid_vector = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "song_vectors"
