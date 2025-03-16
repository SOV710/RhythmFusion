# music/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Song
from .serializers import SongSerializer

import csv
import io


class SongListAPIView(APIView):
    # return all songs
    def get(self, request, format=None):
        songs = Song.objects.all()  # 获取所有歌曲
        # 序列化 QuerySet，指定 many=True
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SongDetailAPIView(APIView):
    # return only one song
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
        # Delete the Song instance with the specified id.
        try:
            song = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UploadCSVView(APIView):
    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get("csv_file")
        if not file_obj:
            return Response(
                {"error": "No CSV file provided."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            file_data = file_obj.read().decode("utf-8", errors="strict")
            # use io.StringIO to wrap the string as a file object
            # so that csv.reader can process it
            csv_file = io.StringIO(file_data)
            csv_reader = csv.reader(csv_file)

            # Convert csv_reader to an iterator to conveniently read the header row first.
            csv_reader = iter(csv_reader)
            header_row = next(csv_reader, None)
            if not header_row:
                return Response(
                    {"error": "CSV file is empty."}, status=status.HTTP_400_BAD_REQUEST
                )

            genre = header_row[-1].strip()

            # Define a set to store already seen songs to prevent duplicates
            # (using the (title, artist) pair as a unique identifier).
            seen_songs = set()
            songs_to_create = []

            for row in csv_reader:
                # If the row has fewer than 2 columns, skip this row.
                if len(row) < 2:
                    continue

                track_name = row[0].strip().strip('"')
                artist_name = row[1].strip().strip('"')

                # prevent duplicates
                song_key = (track_name, artist_name)
                if song_key in seen_songs:
                    continue  # 此歌曲已存在，跳过
                seen_songs.add(song_key)

                # Create a Song object (not written to the database) and assign genre to the school field.
                song = Song(title=track_name, artist=artist_name, school=genre)
                songs_to_create.append(song)

            if not songs_to_create:
                return Response(
                    {"message": "There is no valid song data in the CSV file."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Use database transactions to perform batch writes, ensuring data integrity.
            with transaction.atomic():
                Song.objects.bulk_create(songs_to_create)

            return Response(
                {
                    "message": "CSV文件处理成功！",
                    "inserted_count": len(songs_to_create),
                    "genre": genre,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            # Catch the exception and return the error message.
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
