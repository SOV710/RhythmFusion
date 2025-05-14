# playlist/views.py
import os
import numpy as np
import faiss

from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Playlist
from .serializers import PlaylistSerializer, PlaylistSummarySerializer

from music.serializers import SongSerializer
from music.models import Song
from recommender.models import SongVector


DATA_DIR = os.path.join(settings.BASE_DIR, "recommender", "data")
INDEX_PATH = os.path.join(DATA_DIR, "song_hybrid.index")
MAP_PATH = os.path.join(DATA_DIR, "song_id_map.npy")


_index = None
_song_map = None


def _load_index():
    global _index, _song_map
    if _index is None:
        _index = faiss.read_index(INDEX_PATH)
        _song_map = np.load(MAP_PATH)
    return _index, _song_map


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
        playlist = get_object_or_404(Playlist, pk=pk, owner=request.user)
        song_ids = list(playlist.songs.values_list("id", flat=True))
        if not song_ids:
            return Response([], status=status.HTTP_200_OK)

        # —— 1. 取歌单向量 ——
        vecs = [
            sv.hybrid_vector
            for sv in SongVector.objects.filter(song_id__in=song_ids)
            if sv.hybrid_vector
        ]
        if not vecs:
            return Response([], status=status.HTTP_200_OK)

        arr = np.array(vecs, dtype=np.float32)
        faiss.normalize_L2(arr)
        query = arr.mean(axis=0, keepdims=True)
        faiss.normalize_L2(query)

        # —— 2. 检索 3×10 条候选（足够剔除后仍≥10） ——
        index, song_map = _load_index()
        SEARCH_K = 50  # 检索更大 K
        D, I = index.search(query, SEARCH_K)
        rec_ids = song_map[I[0]].tolist()

        # —— 3. 剔除歌单已有歌曲，再取前 10 ——
        original_set = set(song_ids)
        filtered = [sid for sid in rec_ids if sid not in original_set][:10]

        # 若过滤后不足 10，可按需再扩 K 或直接返回现有结果
        songs = Song.objects.filter(id__in=filtered)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
