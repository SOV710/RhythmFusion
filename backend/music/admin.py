# music/admin.py

from django.contrib import admin
from .models import Song


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    """
    定制 Song 模型在 Django Admin 后台的显示方式。

    list_display: 指定在后台列表中显示的字段。
    search_fields: 允许后台管理人员通过这些字段搜索数据。
    list_filter: 侧边过滤器，便于快速筛选数据。
    """

    list_display = ("title", "artist", "duration")
    search_fields = ("title", "artist")
    list_filter = ("artist",)
