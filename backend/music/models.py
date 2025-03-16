# music/models.py

from django.db import models


class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    school = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} by {self.artist}"
