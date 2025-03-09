# user/apps.py
from django.apps import AppConfig


class UserConfig(AppConfig):
    """
    定义 user 应用的配置信息。

    name: 应用在 Python 包中的名称，必须与文件夹名称一致。
    verbose_name: 后台管理中显示的应用名称。
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "user"
    verbose_name = "用户管理"

    def ready(self):
        pass
