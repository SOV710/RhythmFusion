# music/views.py
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, filters, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import Http404
from django.db.models import Q
import random

from .models import Song, SongLike
from .serializers import SongSerializer, SongUploadSerializer
from .pagination import StandardResultsSetPagination

# 可用的流派列表，直接对应数据库中的值
AVAILABLE_GENRES = [
    "jpop", "blues", "classical", "country", "dance", 
    "electronic", "folk", "hiphop", "jazz", "kpop", 
    "metal", "pop", "punk", "rnb", "rock"
]

GENRE_MAP = {
    "pop": "流行",
    "rock": "摇滚",
    "jazz": "爵士",
    "classical": "古典",
    "hiphop": "嘻哈",
    "electronic": "电子",
    "folk": "民谣",
    "country": "乡村",
    "blues": "蓝调",
    "metal": "金属",
    "jpop": "日本流行",
    "kpop": "韩国流行",
    "rnb": "R&B",
    "punk": "朋克",
    "dance": "舞曲",
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
    Return a list of songs for a specified genre.
    """
    def get(self, request, code, *args, **kwargs):
        # 确保流派代码是小写的
        genre_code = code.lower()
        
        # 检查是否是支持的流派
        if genre_code not in AVAILABLE_GENRES:
            # 如果没有找到匹配的流派，返回404
            return Response(
                {"detail": f"未找到流派: {code}"},
                status=status.HTTP_404_NOT_FOUND
            )
            
        # 构建精确匹配查询
        query = Q(school__iexact=genre_code)
        
        # 查询匹配的歌曲
        matching_songs = Song.objects.filter(query)
        
        # 如果没有找到匹配的歌曲，返回空列表
        if not matching_songs.exists():
            return Response([])
            
        # 随机选择最多10首歌曲
        count = min(matching_songs.count(), 10)
        if count < matching_songs.count():
            # 获取所有ID，然后随机选择
            all_ids = list(matching_songs.values_list('id', flat=True))
            random_ids = random.sample(all_ids, count)
            result_songs = Song.objects.filter(id__in=random_ids)
        else:
            # 如果歌曲数量少于10，直接使用所有匹配的歌曲
            result_songs = matching_songs
            
        # 序列化并返回结果
        serializer = SongSerializer(result_songs, many=True)
        return Response(serializer.data)


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
