# music/urls.py
from django.urls import path
from .views import SongListAPIView, SongDetailAPIView, UploadCSVView

urlpatterns = [
    path("", SongListAPIView.as_view(), name="song-list"),
    path("<int:pk>/", SongDetailAPIView.as_view(), name="song-detail"),
    path("csv/", UploadCSVView.as_view(), name="upload-csv"),
]
