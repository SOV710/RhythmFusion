# recommendation/admin.py

from django.contrib import admin
from .models import RecommendationLog


@admin.register(RecommendationLog)
class RecommendationLogAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "method")
    search_fields = ("user__username", "method")
    list_filter = ("method", "created_at")
