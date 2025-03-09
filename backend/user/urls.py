# user/urls.py
from django.urls import path
from .views import UserRegistrationAPIView, UserProfileAPIView

urlpatterns = [
    # 用户注册接口：
    # 当客户端请求 URL 为 /users/register/ 时，将调用 UserRegistrationAPIView 处理请求
    path("register/", UserRegistrationAPIView.as_view(), name="user-register"),
    # 用户个人信息接口：
    # 当客户端请求 URL 为 /users/profile/ 时，将调用 UserProfileAPIView 处理请求（用于获取和更新个人信息）
    path("profile/", UserProfileAPIView.as_view(), name="user-profile"),
]
