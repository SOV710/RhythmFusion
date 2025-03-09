# user/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    自定义用户模型，继承自 Django 内置的 AbstractUser。
    增加了 bio、birth_date、avatar 等额外字段。
    """

    bio = models.TextField(max_length=500, blank=True, help_text="用户简介")
    birth_date = models.DateField(null=True, blank=True, help_text="出生日期")
    avatar = models.ImageField(
        upload_to="avatars/", null=True, blank=True, help_text="用户头像"
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="创建时间")
    updated_at = models.DateTimeField(auto_now=True, help_text="更新时间")

    class Meta:
        db_table = "users"  # 指定数据库中表的名称

    def __str__(self):
        # 返回用户的用户名作为对象的字符串表示
        return self.username
