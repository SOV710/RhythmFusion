# recommender/management/commands/build_faiss_index.py

import os
import numpy as np
import faiss
from django.core.management.base import BaseCommand
from recommender.models import SongVector

DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data")
os.makedirs(DATA_DIR, exist_ok=True)

INDEX_PATH = os.path.join(DATA_DIR, "song_hybrid.index")
MAP_PATH = os.path.join(DATA_DIR, "song_id_map.npy")


class Command(BaseCommand):
    help = "Build and save FAISS index for hybrid vectors"

    def handle(self, *args, **opts):
        # 1. Collect all hybrid vectors
        entries = SongVector.objects.exclude(hybrid_vector__isnull=True)
        song_ids = []
        vecs = []
        for sv in entries:
            song_ids.append(sv.song_id)
            vecs.append(sv.hybrid_vector)

        vecs = np.array(vecs, dtype=np.float32)
        # 2. Normalize for cosine
        faiss.normalize_L2(vecs)

        # 3. Build Flat IP index
        d = vecs.shape[1]
        index = faiss.IndexFlatIP(d)
        index.add(vecs)

        # 4. Persist
        faiss.write_index(index, INDEX_PATH)
        np.save(MAP_PATH, np.array(song_ids, dtype=np.int64))

        self.stdout.write(
            self.style.SUCCESS(
                f"Built FAISS index ({vecs.shape[0]}×{d}) at {INDEX_PATH}"
            )
        )
