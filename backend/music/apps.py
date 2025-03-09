# music/apps.py

from django.apps import AppConfig


class MusicConfig(AppConfig):
    """
    定义 music 应用的配置信息。

    - name: 应用在 Python 包中的名称，必须与目录名称一致。
    - verbose_name: 后台管理中显示的应用名称。
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "music"
    verbose_name = "音乐管理"

    def ready(self):
        pass
