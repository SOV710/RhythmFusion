# playlist/urls.py
from django.urls import path
from .views import (
    PlaylistCreateView,
    PlaylistDetailView,
    TrackListCreateView,
    TrackDeleteView,
    PlaylistRecommendationView,
)

urlpatterns = [
    # /api/playlists/
    path("", PlaylistCreateView.as_view(), name="playlist-create"),
    # /api/playlists/{id}/
    path("<int:pk>/", PlaylistDetailView.as_view(), name="playlist-detail"),
    # /api/playlists/{id}/tracks/
    path("<int:pk>/tracks/", TrackListCreateView.as_view(), name="playlist-tracks"),
    # /api/playlists/{id}/tracks/{song_id}/
    path(
        "<int:pk>/tracks/<int:song_id>/",
        TrackDeleteView.as_view(),
        name="playlist-track-remove",
    ),
    # /api/playlists/{id}/recommendations/
    path(
        "<int:pk>/recommendations/",
        PlaylistRecommendationView.as_view(),
        name="playlist-recommendations",
    ),
]
