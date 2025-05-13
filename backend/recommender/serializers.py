# music/serializers.py

from rest_framework import serializers
from .models import SongLike


class SongLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongLike
        fields = ["id", "song", "created_at"]
        read_only_fields = ["id", "created_at"]
