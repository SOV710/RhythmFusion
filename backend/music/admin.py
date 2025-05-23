# music/admin.py

from django.contrib import admin
from .models import Song


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "school")
    search_fields = ("title", "artist")
    list_filter = ("artist",)
