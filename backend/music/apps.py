# music/apps.py

from django.apps import AppConfig


class MusicConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "music"
    verbose_name = "音乐管理"

    def ready(self):
        pass
