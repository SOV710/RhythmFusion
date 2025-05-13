# music/views.py

from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SongLike, Song
from .serializers import SongLikeSerializer


class SongLikeToggleView(APIView):
    """
    POST   /api/music/{song_id}/like/   → 点赞
    DELETE /api/music/{song_id}/like/   → 取消点赞
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, song_id):
        song = get_object_or_404(Song, pk=song_id)
        like, created = SongLike.objects.get_or_create(
            user=request.user, song=song)
        if created:
            serializer = SongLikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": "already liked"}, status=status.HTTP_200_OK)

    def delete(self, request, song_id):
        like_qs = SongLike.objects.filter(user=request.user, song_id=song_id)
        if not like_qs.exists():
            return Response(
                {"detail": "not liked before"}, status=status.HTTP_400_BAD_REQUEST
            )
        like_qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
