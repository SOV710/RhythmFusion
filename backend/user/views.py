# user/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
)


# ---------- Profile ----------
class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/user/profile   -> 查看自己资料
    PATCH/PUT 同 URL        -> 修改资料
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # request.user 已由 JWTAuthentication 注入
        return self.request.user


# ---------- Register ----------
class UserRegistrationAPIView(generics.CreateAPIView):
    """
    POST body: {username, email?, password}
    """

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# ---------- Login ----------
class UserLoginAPIView(TokenObtainPairView):
    """
    ▶ POST /api/user/login
    body: {username, password}
    resp: {refresh, access}
    """

    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]


# ---------- Logout ----------
class UserLogoutAPIView(APIView):
    """
    客户端携带 refresh token 调用即可将其拉黑：
    POST body: {"refresh": "<refresh_token>"}
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if refresh_token is None:
            return Response(
                {"detail": "refresh token required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # 需要 token_blacklist app
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except TokenError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
