# playlist/serializers.py
from rest_framework import serializers
from .models import Playlist
from music.models import Song


class PlaylistSerializer(serializers.ModelSerializer):
    song_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        write_only=True,
        required=False,  # 允许“只建歌单不加歌”
        help_text="一次性添加到歌单的歌曲 ID 列表",
    )

    class Meta:
        model = Playlist
        fields = ["id", "name", "song_ids", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        song_ids = validated_data.pop("song_ids", [])
        playlist = Playlist.objects.create(**validated_data)
        if song_ids:
            songs = Song.objects.filter(id__in=song_ids)
            playlist.songs.add(*songs)
        return playlist


class PlaylistSummarySerializer(serializers.ModelSerializer):
    """
    列出歌单时只需要 id 和 name
    """

    class Meta:
        model = Playlist
        fields = ["id", "name"]
        read_only_fields = ["id", "name"]
