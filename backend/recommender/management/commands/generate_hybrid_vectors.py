# recommender/management/commands/generate_hybrid_vectors.py

import numpy as np
from django.core.management.base import BaseCommand
from recommender.models import SongVector
from django.db import transaction


class Command(BaseCommand):
    help = "Generate hybrid_vector = [cf_vector; content_vector] with null handling"

    def handle(self, *args, **opts):
        updated = 0
        with transaction.atomic():
            for sv in SongVector.objects.all():
                cf = sv.cf_vector or []
                ct = sv.content_vector or []

                # 当 cf 全为空时，hybrid=content
                if not cf:
                    hybrid = ct
                # 当 content 全为空时，hybrid=cf
                elif not ct:
                    hybrid = cf
                else:
                    # cf 或 ct 都是 list of numbers
                    cf_arr = np.array(cf, dtype=np.float32)
                    ct_arr = np.array(ct, dtype=np.float32)
                    hybrid_arr = np.concatenate([cf_arr, ct_arr])
                    hybrid = hybrid_arr.tolist()

                SongVector.objects.filter(
                    song=sv.song).update(hybrid_vector=hybrid)
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(f"Updated hybrid_vector for {updated} songs.")
        )
