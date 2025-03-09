# user/admin.py
from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    自定义 User 模型在后台的显示配置。

    list_display: 后台列表页显示的字段
    search_fields: 可用于搜索的字段
    list_filter: 可用于侧边过滤的字段
    """

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "created_at",
    )
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
