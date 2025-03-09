# music/serializers.py

from rest_framework import serializers
from .models import Song


class SongSerializer(serializers.ModelSerializer):
    """
    歌曲序列化器：
    将 Song 模型实例转换为 Python 原生数据类型（如字典），
    方便后续渲染成 JSON 数据，或反序列化创建/更新 Song 实例。
    """

    class Meta:
        model = Song  # 指定序列化的模型
        fields = ("id", "title", "artist", "duration")  # 指定需要序列化的字段
