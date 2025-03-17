# playlist/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Playlist
from .serializers import PlaylistSerializer
from django.shortcuts import get_object_or_404


class PlaylistListAPIView(APIView):
    # The frontend can decide based on whether the returned playlists array is empty:
    # if it's empty, display a box in the window with "create your playlist".
    # if it's not empty, display all playlists normally and additionally show a "create your playlist" box below the list.
    def get(self, request, format=None):
        # 过滤出当前登录用户的歌单
        playlists = Playlist.objects.filter(user=request.user)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(
            {"playlists": serializer.data, "placeholder": "create your playlist"},
            status=status.HTTP_200_OK,
        )

    def post(self, request, format=None):
        # 创建新的歌单时，自动将当前登录用户作为创建者
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaylistDetailAPIView(APIView):
    def get(self, request, pk, format=None):
        playlist = get_object_or_404(Playlist, pk=pk, user=request.user)
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        playlist = get_object_or_404(Playlist, pk=pk, user=request.user)
        serializer = PlaylistSerializer(
            playlist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # 更新歌单信息
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        playlist = get_object_or_404(Playlist, pk=pk, user=request.user)
        playlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
