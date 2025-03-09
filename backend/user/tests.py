# user/tests.py

from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_user_str(self):
        # 测试 __str__ 方法是否返回用户名
        self.assertEqual(str(self.user), "testuser")

    def test_user_creation(self):
        # 测试用户是否成功创建，并检查字段
        self.assertTrue(self.user.check_password("testpass123"))
        self.assertEqual(self.user.email, "test@example.com")
