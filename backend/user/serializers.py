# user/serializers.py

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """公共资料字段；用于 profile GET / PATCH。"""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "birth_date",
            "avatar",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class RegisterSerializer(serializers.ModelSerializer):
    """POST /api/user/register"""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        # 用 set_password 以哈希形式保存密码
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(TokenObtainPairSerializer):
    """
    继承 simplejwt 的 TokenObtainPairSerializer：
    - 校验 username / password
    - 成功后返回 access 与 refresh
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # 可以在 token 内塞自定义声明
        token["username"] = user.username
        return token
