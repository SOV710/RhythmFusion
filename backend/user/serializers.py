# user/serializers.py

from django.contrib.auth import get_user_model
from rest_framework import serializers

# 获取自定义 User 模型
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # 这里可以添加额外的字段或方法，处理密码写入等
    class Meta:
        model = User
        # 注意：password 字段应设置为 write_only，不返回给前端
        fields = ("id", "username", "email", "password",
                  "bio", "birth_date", "avatar")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)  # 对密码进行加密
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
