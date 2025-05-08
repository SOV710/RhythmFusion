# playlist/admin.py

from django.contrib import admin
from .models import Playlist


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("name", "owner")
    search_fields = ("name", "user__username")
    list_filter = ("owner",)
