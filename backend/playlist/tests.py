# playlist/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from music.models import Song
from .models import Playlist
from datetime import timedelta


class PlaylistModelTest(TestCase):
    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create_user(
            username="testuser", password="testpass")
        # 创建测试歌曲
        self.song1 = Song.objects.create(
            title="Song One", artist="Artist A", duration=timedelta(minutes=3)
        )
        self.song2 = Song.objects.create(
            title="Song Two", artist="Artist B", duration=timedelta(minutes=4)
        )
        # 创建歌单，并添加歌曲
        self.playlist = Playlist.objects.create(
            name="My Playlist", user=self.user)
        self.playlist.songs.add(self.song1, self.song2)

    def test_playlist_str(self):
        # 测试 __str__ 方法是否返回正确格式字符串
        expected_str = f"My Playlist by {self.user.username}"
        self.assertEqual(str(self.playlist), expected_str)

    def test_playlist_songs(self):
        # 测试歌单中歌曲是否添加成功
        self.assertEqual(self.playlist.songs.count(), 2)
