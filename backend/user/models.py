# user/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True, help_text="用户简介")
    birth_date = models.DateField(null=True, blank=True, help_text="出生日期")
    avatar = models.ImageField(
        upload_to="avatars/", null=True, blank=True, help_text="用户头像"
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="创建时间")
    updated_at = models.DateTimeField(auto_now=True, help_text="更新时间")

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username
