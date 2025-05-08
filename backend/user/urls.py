# user/urls.py
from django.urls import path
from .views import (
    UserProfileAPIView,
    UserLoginAPIView,
    UserRegistrationAPIView,
    UserLogoutAPIView,
    UserTokenRefreshAPIView,
    UserTokenVerifyAPIView,
)

urlpatterns = [
    path("profile/", UserProfileAPIView.as_view(), name="user-profile"),
    path("login/", UserLoginAPIView.as_view(), name="user-login"),
    path("register/", UserRegistrationAPIView.as_view(), name="user-register"),
    path("logout/", UserLogoutAPIView.as_view(), name="user-logout"),
    path("refresh/", UserTokenRefreshAPIView.as_view(), name="user-token-refresh"),
    path("verify/", UserTokenVerifyAPIView.as_view(), name="user-token-verify"),
]
