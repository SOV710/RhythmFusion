# recommendation/models.py

from django.db import models
from django.conf import settings


class RecommendationLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recommendation_logs",
        help_text="计算推荐结果的用户",
    )
    method = models.CharField(max_length=50, help_text="推荐算法方法，如 'hybrid'")
    results = models.TextField(help_text="推荐结果的 JSON 格式字符串")
    created_at = models.DateTimeField(auto_now_add=True, help_text="计算时间")

    class Meta:
        db_table = "recommendation_log"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Recommendation for {self.user.username} at {self.created_at}"
