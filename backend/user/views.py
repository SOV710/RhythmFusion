# user/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationAPIView(APIView):
    def post(self, request, format=None):
        # request.data 中已经包含前端传来的 JSON 数据
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # 调用 create() 方法创建用户
            # 返回用户数据，状态码 201 Created
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        # 验证失败则返回错误信息和 400 状态码
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(APIView):
    """
    用户个人信息 API 视图：
    仅允许已登录用户访问，用于获取或更新用户信息
    """

    def get(self, request, format=None):
        # 假设当前登录用户存放在 request.user 中
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request, format=None):
        # 更新当前登录用户的信息，实例为 request.user
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()  # 调用 update() 方法更新用户
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
