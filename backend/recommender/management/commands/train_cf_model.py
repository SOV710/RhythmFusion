# recommender/management/commands/train_cf_model.py

import os
import json
import scipy.sparse as sp
from django.core.management.base import BaseCommand
from sklearn.decomposition import TruncatedSVD
from recommender.models import SongVector
from django.db import transaction

DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data")


class Command(BaseCommand):
    help = "Train CF model (SVD) and write cf_vector into SongVector"

    def add_arguments(self, parser):
        parser.add_argument(
            "--factors", type=int, default=50, help="Number of latent factors K"
        )

    def handle(self, *args, **opts):
        K = opts["factors"]
        # 1. Load COO
        coo = sp.load_npz(os.path.join(DATA_DIR, "interaction_coo.npz"))
        csr = coo.tocsr()

        # 2. SVD: items × users => transpose then n_components=K
        svd = TruncatedSVD(n_components=K, n_iter=10, random_state=42)
        item_factors = svd.fit_transform(csr.T)  # shape = (n_songs, K)

        # 3. Load song_ids mapping
        with open(os.path.join(DATA_DIR, "user_song_map.json")) as f:
            mapping = json.load(f)
        song_ids = mapping["song_ids"]

        # 4. Write cf_vector back
        with transaction.atomic():
            for idx, song_id in enumerate(song_ids):
                vec = item_factors[idx].tolist()
                SongVector.objects.update_or_create(
                    song_id=song_id, defaults={"cf_vector": vec}
                )

        self.stdout.write(
            self.style.SUCCESS(f"Trained SVD(K={K}) and wrote cf_vector for {len(song_ids)} songs.")
        )
