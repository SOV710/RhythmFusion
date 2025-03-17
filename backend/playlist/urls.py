# playlist/urls.py
from django.urls import path
from .views import PlaylistListAPIView, PlaylistDetailAPIView

urlpatterns = [
    path("", PlaylistListAPIView.as_view(), name="playlist-list"),
    path("<int:pk>/", PlaylistDetailAPIView.as_view(), name="playlist-detail"),
]
