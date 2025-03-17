# playlist/serializers.py

from rest_framework import serializers
from .models import Playlist
from music.serializers import SongSerializer  # 引入已有的 Song 序列化器


class PlaylistSerializer(serializers.ModelSerializer):
    # 方案一：仅返回歌曲主键
    # songs = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=SongSerializer.Meta.model.objects.all()
    # )

    # 方案二：使用嵌套序列化，显示歌曲的详细信息
    songs = SongSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = ("id", "name", "user", "songs")
        # 若需要让 user 字段显示为用户名，可自定义
        extra_kwargs = {
            "user": {"read_only": True}  # 通过后端认证后确定用户
        }
