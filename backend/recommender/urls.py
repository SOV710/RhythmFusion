# music/urls.py

from django.urls import path
from .views import SongLikeToggleView

urlpatterns = [
    # … 你现有的其它 music 路由 …
    # 点赞 / 取消点赞
    path(
        "music/<int:song_id>/like/",
        SongLikeToggleView.as_view(),
        name="song-like-toggle",
    ),
]
