# music/serializers.py

from rest_framework import serializers
from .models import Song, SongLike


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ["id", "title", "artist", "school"]


class SongUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ["title", "artist", "school"]


class SongLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongLike
        fields = ["song", "created_at"]
        read_only_fields = ["created_at"]
