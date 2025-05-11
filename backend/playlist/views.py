# playlist/views.py
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Playlist
from .serializers import PlaylistSerializer, PlaylistSummarySerializer
from music.serializers import SongSerializer
from music.models import Song


# ---------- POST /api/playlists/ ----------
class PlaylistCreateView(generics.CreateAPIView):
    """
    创建歌单；请求体仅需 {"name": "..."}
    """

    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # 绑定当前登录用户为 owner
        serializer.save(owner=self.request.user)


class PlaylistListView(generics.ListAPIView):
    """
    GET /api/playlists/list/
    列出当前用户所有歌单的 id 和 name
    """

    serializer_class = PlaylistSummarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)


# ---------- GET /api/playlists/{id}/ ----------
class PlaylistDetailView(generics.RetrieveAPIView):
    """
    仅允许歌单所有者查看
    """

    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 只能看到自己的歌单
        return Playlist.objects.filter(owner=self.request.user)


# ---------- GET | POST /api/playlists/{id}/tracks/ ----------
class TrackListCreateView(APIView):
    """
    GET  → 列出歌单中的歌曲
    POST → 向歌单添加歌曲  {"song_id": 123}
    """

    permission_classes = [permissions.IsAuthenticated]

    def _get_playlist(self, request, pk):
        return get_object_or_404(Playlist, pk=pk, owner=request.user)

    def get(self, request, pk):
        playlist = self._get_playlist(request, pk)
        serializer = SongSerializer(playlist.songs.all(), many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        playlist = self._get_playlist(request, pk)
        ids = request.data.get("song_ids") or request.data.get("song_id")
        if not ids:
            return Response({"detail": "song_ids required"}, status=400)

        # 兼容单个和列表两种写法
        if not isinstance(ids, list):
            ids = [ids]

        songs = Song.objects.filter(id__in=ids)
        playlist.songs.add(*songs)
        return Response({"detail": "songs added"}, status=201)


# ---------- DELETE /api/playlists/{id}/tracks/{song_id}/ ----------
class TrackDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, song_id):
        playlist = get_object_or_404(Playlist, pk=pk, owner=request.user)
        song = get_object_or_404(Song, pk=song_id)
        playlist.songs.remove(song)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------- GET /api/playlists/{id}/recommendations/ ----------
class PlaylistRecommendationView(APIView):
    """
    先留空，后续实现推荐逻辑
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        # TODO: 实际推荐代码
        return Response(
            {"detail": "Not implemented yet."},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )
