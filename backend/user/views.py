# user/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

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


class UserTokenRefreshAPIView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]


class UserTokenVerifyAPIView(TokenVerifyView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        token_str = request.data.get("token")
        if not token_str:
            return Response(
                {"detail": "No token provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # 1. 调用父类做基础校验（签名、exp、nbf…）
        try:
            super().post(request, *args, **kwargs)
        except InvalidToken as e:
            # 签名或过期失败
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        # 2. 用 RefreshToken API 解析出 jti 并检查黑名单
        try:
            rt = RefreshToken(token_str)
            jti = rt["jti"]
        except TokenError:
            # 不是合法的 refresh token，就按非黑名单处理，通过即可
            return Response({}, status=status.HTTP_200_OK)

        # 3. 查询是否在黑名单中
        try:
            outstanding = OutstandingToken.objects.get(jti=jti)
        except OutstandingToken.DoesNotExist:
            # 如果数据库中找不到，说明这个 token 从未发放过 → 视作无效
            return Response(
                {"detail": "Token not recognized"}, status=status.HTTP_401_UNAUTHORIZED
            )

        if BlacklistedToken.objects.filter(token=outstanding).exists():
            return Response(
                {"detail": "Token has been blacklisted"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # 4. 全部通过
        return Response({}, status=status.HTTP_200_OK)
