# recommender/management/commands/generate_content_vectors.py

import json
from django.core.management.base import BaseCommand
from django.db import transaction
from music.models import Song
from recommender.models import SongVector


class Command(BaseCommand):
    help = "为每首歌生成 One-Hot content_vector 并写入 song_vectors 表"

    def handle(self, *args, **options):
        # 1. 收集所有歌曲的 artist 和 school
        songs = list(Song.objects.all().values("id", "artist", "school"))
        artists = sorted({rec["artist"] for rec in songs})
        schools = sorted({rec["school"] for rec in songs})

        # 2. 构建 One-Hot 索引
        artist_idx = {a: i for i, a in enumerate(artists)}
        school_idx = {s: i for i, s in enumerate(schools)}
        vector_len = len(artists) + len(schools)

        # —— 下面这一行确保完整闭合 f-string ——
        self.stdout.write(
            self.style.NOTICE(
                f"Found {len(artists)} artists, {len(schools)} schools, vector_len={vector_len}"
            )
        )

        # 3. 用事务批量写入/更新 content_vector
        with transaction.atomic():
            for rec in songs:
                song_id = rec["id"]
                vector = [0] * vector_len
                art, sch = rec["artist"], rec["school"]
                if art in artist_idx:
                    vector[artist_idx[art]] = 1
                if sch in school_idx:
                    vector[len(artists) + school_idx[sch]] = 1

                SongVector.objects.update_or_create(
                    song_id=song_id, defaults={"content_vector": vector}
                )

        self.stdout.write(
            self.style.SUCCESS("All content_vectors have been generated and saved.")
        )
