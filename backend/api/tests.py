# api/tests.py

from django.test import TestCase


class APIRoutesTest(TestCase):
    def test_users_route(self):
        response = self.client.get("/api/users/")
        # 检查接口是否存在（非 404）
        self.assertNotEqual(response.status_code, 404)

    def test_songs_route(self):
        response = self.client.get("/api/songs/")
        self.assertNotEqual(response.status_code, 404)

    def test_playlists_route(self):
        response = self.client.get("/api/playlists/")
        self.assertNotEqual(response.status_code, 404)

    def test_recommendations_route(self):
        response = self.client.get("/api/recommendations/")
        self.assertNotEqual(response.status_code, 404)
