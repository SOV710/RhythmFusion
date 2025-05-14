# music/urls.py
from django.urls import path
from .views import (
    SongSearchView,
    UploadView,
    GenreRecommendationView,
    SongLikeToggleView,
    UserLikedSongsView,
    LikedSongDeleteView,
)

urlpatterns = [
    path("", SongSearchView.as_view(), name="song-search"),
    path("upload/", UploadView.as_view(), name="song-upload"),
    path("<int:song_id>/like/", SongLikeToggleView.as_view(), name="song-like"),
    path(
        "genres/<str:code>/",
        GenreRecommendationView.as_view(),
        name="song-genre-recommend",
    ),
    path("likes/", UserLikedSongsView.as_view(), name="user-liked-songs"),
    path("likes/<int:song_id>/", LikedSongDeleteView.as_view(), name="liked-song-delete"),
]
