# music/urls.py
from django.urls import path
from .views import SongSearchView, UploadCSVView, GenreRecommendationView

urlpatterns = [
    path("", SongSearchView.as_view(), name="song-search"),
    path("csv/", UploadCSVView.as_view(), name="song-upload"),
    path(
        "genres/<str:code>/",
        GenreRecommendationView.as_view(),
        name="song-genre-recommend",
    ),
]
