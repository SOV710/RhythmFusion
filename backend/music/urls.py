# music/urls.py
from django.urls import path
from .views import SongSearchView, UploadView, GenreRecommendationView

urlpatterns = [
    path("", SongSearchView.as_view(), name="song-search"),
    path("upload/", UploadView.as_view(), name="song-upload"),
    path(
        "genres/<str:code>/",
        GenreRecommendationView.as_view(),
        name="song-genre-recommend",
    ),
]
