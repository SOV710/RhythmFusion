# music/views.py

import csv
import io

from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db import transaction
from django.http import Http404

from .models import Song
from .serializers import SongSerializer

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

    pagination_class = None  # ← disables pagination per requirement


class UploadCSVView(APIView):
    def post(self, request, *args, **kwargs):
        # 1. grab the uploaded file object from the multipart/form-data payload
        file_obj = request.FILES.get("csv_file")
        if not file_obj:
            # 2. if no file was sent, bail out with 400
            return Response(
                {"error": "No CSV file provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # 3. read ALL bytes and decode them into a Python str
            #    – request.FILES gives you a Django InMemoryUploadedFile or TemporaryUploadedFile,
            #      whose .read() returns raw bytes from the client’s upload.
            file_data = file_obj.read().decode("utf-8", errors="strict")

            # 4. wrap that raw string in StringIO, so csv.reader can do .readline(), iteration, etc.
            #    – csv.reader expects an iterable of text lines (a “file‐like” object).
            csv_file = io.StringIO(file_data)

            # 5. hand it to the CSV parser
            csv_reader = csv.reader(csv_file)

            # 6. pull off the first row as the header, so we can extract the genre
            csv_reader = iter(csv_reader)
            header_row = next(csv_reader, None)
            if not header_row:
                return Response(
                    {"error": "CSV file is empty."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            genre = header_row[-1].strip()

            # 7. loop over each remaining row, skip invalid ones, dedupe by (title,artist)
            seen_songs = set()
            songs_to_create = []
            for row in csv_reader:
                if len(row) < 2:
                    continue
                track_name = row[0].strip().strip('"')
                artist_name = row[1].strip().strip('"')
                key = (track_name, artist_name)
                if key in seen_songs:
                    continue
                seen_songs.add(key)
                # 8. build Song instances in memory
                songs_to_create.append(
                    Song(title=track_name, artist=artist_name, school=genre)
                )

            # 9. if nothing valid was found, return 400
            if not songs_to_create:
                return Response(
                    {"message": "There is no valid song data in the CSV file."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 10. atomically bulk‐insert them into the database
            with transaction.atomic():
                Song.objects.bulk_create(songs_to_create)

            # 11. success response with count and genre
            return Response(
                {
                    "message": "CSV file processed successfully!",
                    "inserted_count": len(songs_to_create),
                    "genre": genre,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            # 12. catch any error (e.g. bad decode, CSV parse error) and return it
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
