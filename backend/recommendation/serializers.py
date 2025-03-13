# recommendation/serializers.py

from rest_framework import serializers
from .models import RecommendationLog


class RecommendationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationLog
        fields = ("id", "user", "method", "results", "created_at")
        extra_kwargs = {"user": {"read_only": True}}
