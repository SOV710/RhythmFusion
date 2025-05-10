# music/serializers.py

from rest_framework import serializers
from .models import Song


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ["id", "title", "artist", "school"]


class SongUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ["title", "artist", "school"]
