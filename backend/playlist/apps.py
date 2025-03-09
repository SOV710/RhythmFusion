# playlist/apps.py

from django.apps import AppConfig


class PlaylistConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "playlist"
    verbose_name = "歌单管理"

    def ready(self):
        pass
