# playlist/urls.py
from django.urls import path
from .views import PlaylistListAPIView, PlaylistDetailAPIView

urlpatterns = [
    # 歌单列表接口：
    # 当客户端请求 URL 为 /playlists/ 时，将调用 PlaylistListAPIView 返回当前登录用户的所有歌单，
    # 同时支持通过 POST 请求创建新的歌单
    path("", PlaylistListAPIView.as_view(), name="playlist-list"),
    # 歌单详情接口：
    # 当客户端请求 URL 为 /playlists/<int:pk>/ 时，将调用 PlaylistDetailAPIView
    # 用于获取、更新或删除单个歌单
    path("<int:pk>/", PlaylistDetailAPIView.as_view(), name="playlist-detail"),
]
