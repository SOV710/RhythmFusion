# music/urls.py
from django.urls import path
from .views import SongListAPIView, SongDetailAPIView, UploadCSVView

urlpatterns = [
    # 调用 SongListAPIView 返回所有歌曲数据
    path("", SongListAPIView.as_view(), name="song-list"),
    # 调用 SongDetailAPIView 返回单个歌曲的详情
    path("<int:pk>/", SongDetailAPIView.as_view(), name="song-detail"),
    path("csv/", UploadCSVView.as_view(), name="upload-csv"),
]
