# user/urls.py
from django.urls import path
from .views import UserRegistrationAPIView, UserProfileAPIView

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="user-register"),
    path("profile/", UserProfileAPIView.as_view(), name="user-profile"),
]
