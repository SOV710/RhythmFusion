# recommender/management/commands/build_interaction_matrix.py

import os
import json
import numpy as np
import scipy.sparse as sp
from django.core.management.base import BaseCommand
from music.models import Song
from music.models import SongLike  # adjust import path if needed
from django.contrib.auth import get_user_model

DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data")
os.makedirs(DATA_DIR, exist_ok=True)


class Command(BaseCommand):
    help = "Build user–song interaction COO matrix from SongLike"

    def handle(self, *args, **opts):
        User = get_user_model()

        # 1. Collect all users and songs
        user_ids = list(User.objects.values_list("id", flat=True))
        song_qs = Song.objects.values_list("id", flat=True)
        song_ids = list(song_qs)

        u2i = {u: i for i, u in enumerate(user_ids)}
        s2j = {s: j for j, s in enumerate(song_ids)}

        # 2. Build COO data
        likes = SongLike.objects.values_list("user_id", "song_id")
        rows, cols = [], []
        for u, s in likes:
            if u in u2i and s in s2j:
                rows.append(u2i[u])
                cols.append(s2j[s])

        data = np.ones(len(rows), dtype=np.float32)
        coo = sp.coo_matrix((data, (rows, cols)), shape=(
            len(user_ids), len(song_ids)))

        # 3. Persist
        coo_path = os.path.join(DATA_DIR, "interaction_coo.npz")
        sp.save_npz(coo_path, coo)

        # 4. Save mapping
        with open(os.path.join(DATA_DIR, "user_song_map.json"), "w") as f:
            json.dump({"user_ids": user_ids, "song_ids": song_ids}, f)

        self.stdout.write(
            self.style.SUCCESS(
                f"Saved COO to {coo_path}, mappings to user_song_map.json"
            )
        )
