# api/urls.py

from django.urls import path, include

urlpatterns = [
    path("users/", include("user.urls")),
    path("songs/", include("music.urls")),
    path("playlists/", include("playlist.urls")),
    path("recommendations/", include("recommendation.urls")),
]
