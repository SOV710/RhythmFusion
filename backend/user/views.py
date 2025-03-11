# user/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny

User = get_user_model()


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        # 获取请求中的用户名和密码
        username = request.data.get("username")
        password = request.data.get("password")

        # 使用 Django 内置的 authenticate 方法进行认证
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)

            return Response(
                {
                    "username": user.username,
                    "email": user.email,
                    "bio": user.bio,
                    "birth_date": user.birth_date,
                    "avatar": user.avatar.url if user.avatar else None,
                },
                status=status.HTTP_200_OK,
            )
        else:
            # If failed, return the error info
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )


class UserRegistrationAPIView(APIView):
    def post(self, request, format=None):
        # request.data contain the JSON data from frontend
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Return user data，201 Created
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        # if failed, return the error info and 400 code
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(APIView):
    def get(self, request, format=None):
        # Assume that the registered user is in request.user
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request, format=None):
        # refresh the logined user info，instance is request.user
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()  # 调用 update() 方法更新用户
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
