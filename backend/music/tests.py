# music/tests.py

from django.test import TestCase
from .models import Song
from datetime import timedelta


class SongModelTest(TestCase):
    def setUp(self):
        # 创建一个 Song 实例供测试使用
        self.song = Song.objects.create(
            title="Test Song",
            artist="Test Artist",
            duration=timedelta(minutes=3, seconds=30),
        )

    def test_song_str(self):
        # 测试 __str__ 方法是否正确返回字符串表示
        expected_str = "Test Song by Test Artist"
        self.assertEqual(str(self.song), expected_str)

    def test_song_fields(self):
        # 测试歌曲字段是否存储正确
        self.assertEqual(self.song.title, "Test Song")
        self.assertEqual(self.song.artist, "Test Artist")
        self.assertEqual(self.song.duration, timedelta(minutes=3, seconds=30))
