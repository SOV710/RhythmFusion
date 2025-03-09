# music/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Song
from .serializers import SongSerializer


class SongListAPIView(APIView):
    """
    API 视图：返回所有歌曲列表
    GET 请求时查询所有 Song 实例，并使用 SongSerializer 进行序列化后返回 JSON 数据。
    """

    def get(self, request, format=None):
        songs = Song.objects.all()  # 获取所有歌曲
        # 序列化 QuerySet，指定 many=True
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SongDetailAPIView(APIView):
    """
    API 视图：返回单个歌曲详情
    根据 URL 中的歌曲 id 查询 Song 实例，序列化后返回 JSON 数据。
    """

    def get(self, request, pk, format=None):
        try:
            song = Song.objects.get(pk=pk)  # 根据主键获取 Song 实例
        except Song.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        # 更新指定 id 的 Song 实例
        try:
            song = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = SongSerializer(song, data=request.data)
        if serializer.is_valid():
            serializer.save()  # 更新操作
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        # 删除指定 id 的 Song 实例
        try:
            song = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
