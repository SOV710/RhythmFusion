# recommendation/admin.py

from django.contrib import admin
from .models import RecommendationLog


@admin.register(RecommendationLog)
class RecommendationLogAdmin(admin.ModelAdmin):
    """
    可选：记录推荐计算的日志，便于调试和统计
    """

    list_display = ("user", "created_at", "method")
    search_fields = ("user__username", "method")
    list_filter = ("method", "created_at")
