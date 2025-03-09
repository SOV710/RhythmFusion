# recommendation/apps.py

from django.apps import AppConfig


class RecommendationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "recommendation"
    verbose_name = "推荐算法模块"

    def ready(self):
        # 如果需要注册信号或初始化操作，可以在这里执行
        pass
