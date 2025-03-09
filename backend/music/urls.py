# music/urls.py
from django.urls import path
from .views import SongListAPIView, SongDetailAPIView

urlpatterns = [
    # 歌曲列表接口：
    # 当客户端请求 URL 为 /songs/ 时，将调用 SongListAPIView 返回所有歌曲数据
    path("", SongListAPIView.as_view(), name="song-list"),
    # 歌曲详情接口：
    # 当客户端请求 URL 为 /songs/<int:pk>/ 时，将调用 SongDetailAPIView 返回单个歌曲的详情
    path("<int:pk>/", SongDetailAPIView.as_view(), name="song-detail"),
]
