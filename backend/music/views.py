# music/views.py
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, filters, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import Http404

from .models import Song, SongLike
from .serializers import SongSerializer, SongUploadSerializer
from .pagination import StandardResultsSetPagination

GENRE_MAP = {
    "pop": [1, 2, 3],
    "rock": [4, 5],
    "jazz": [6, 7, 8],
}


class SongSearchView(generics.ListAPIView):
    """
    Read-only list with simple keyword search on title / artist / school.
    Inherits *ListAPIView* to get pagination off by default and
    to keep the view minimal.
    """

    serializer_class = SongSerializer
    queryset = Song.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "artist", "school"]  # maps to ?search=

    pagination_class = StandardResultsSetPagination


class UploadView(APIView):
    def post(self, request, format=None):
        raw = request.data
        if not isinstance(raw, list):
            return Response(
                {"detail": "Expected a JSON array."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 把带空格的键 → title / artist / school
        normalized = []
        for idx, item in enumerate(raw, start=1):
            try:
                normalized.append(
                    {
                        "title": item["Track name"],
                        "artist": item["Artist name"],
                        "school": item.get("School", "未知流派"),
                    }
                )
            except KeyError as e:
                return Response(
                    {"detail": f"Item #{idx} missing key: {e}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # many=True 批量校验 & 保存
        serializer = SongUploadSerializer(data=normalized, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # 每行都 insert，一般足够；如需极致性能可自行改 bulk_create

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GenreRecommendationView(APIView):
    """
    Return the predefined song set for a fixed genre code.
    """

    def get(self, request, code, *args, **kwargs):
        song_ids = GENRE_MAP.get(code)
        if song_ids is None:
            raise Http404("Unknown genre code.")
        songs = Song.objects.filter(id__in=song_ids)
        return Response(SongSerializer(songs, many=True).data)


class SongLikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, song_id):
        song = get_object_or_404(Song, pk=song_id)
        like, created = SongLike.objects.get_or_create(user=request.user, song=song)
        if created:
            return Response({"detail": "liked"}, status=status.HTTP_201_CREATED)
        return Response({"detail": "already liked"}, status=status.HTTP_200_OK)

    def delete(self, request, song_id):
        song = get_object_or_404(Song, pk=song_id)
        deleted, _ = SongLike.objects.filter(user=request.user, song=song).delete()
        if deleted:
            return Response({"detail": "unliked"}, status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "not liked before"}, status=status.HTTP_400_BAD_REQUEST
        )


class UserLikedSongsView(APIView):
    """
    Return all songs that the current user has liked.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # 获取用户喜欢的所有SongLike对象
        liked_song_ids = SongLike.objects.filter(user=request.user).values_list('song_id', flat=True)
        # 获取对应的Song对象
        songs = Song.objects.filter(id__in=liked_song_ids)
        # 序列化并返回结果
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)


class LikedSongDeleteView(APIView):
    """
    Delete a specific liked song for the current user.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, song_id):
        # 尝试找到用户喜欢的这首歌
        try:
            like = SongLike.objects.get(user=request.user, song_id=song_id)
            like.delete()
            return Response({"detail": "已从收藏列表中移除"}, status=status.HTTP_204_NO_CONTENT)
        except SongLike.DoesNotExist:
            return Response({"detail": "未找到此收藏歌曲"}, status=status.HTTP_404_NOT_FOUND)
