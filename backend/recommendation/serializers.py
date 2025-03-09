# recommendation/serializers.py

from rest_framework import serializers
from .models import RecommendationLog


class RecommendationLogSerializer(serializers.ModelSerializer):
    """
    推荐日志序列化器：
    用于将 RecommendationLog 模型实例转换为 JSON 数据。
    """

    class Meta:
        model = RecommendationLog
        fields = ("id", "user", "method", "results", "created_at")
        extra_kwargs = {"user": {"read_only": True}}
