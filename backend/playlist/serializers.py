# playlist/serializers.py
from rest_framework import serializers
from .models import Playlist


class PlaylistSerializer(serializers.ModelSerializer):
    """
    用于创建 / 查看歌单基本信息（不嵌入歌曲列表，
    歌曲详情接口由 /tracks/ 单独承担）
    """

    class Meta:
        model = Playlist
        fields = ["id", "name", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
