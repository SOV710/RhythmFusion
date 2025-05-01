# user/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth import get_user_model, authenticate, login

User = get_user_model()


class UserProfileAPIView(APIView):
    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request, format=None):
        # 更新当前登录用户的信息，实例为 request.user
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()  # 调用 update() 方法更新用户
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")

        # Confirm that user input username and password
        if not username or not password:
            return Response(
                {"error": "Give me your fucking USERNAME and PASSWORD"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # verify the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Username or password is wrong"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class UserRegistrationAPIView(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):
    pass
