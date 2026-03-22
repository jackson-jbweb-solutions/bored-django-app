# tasks/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseLayoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

    def test_task_list_renders_dark_sidebar(self):
        response = self.client.get("/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "bg-slate-900")
        self.assertContains(response, "bg-slate-950")

    def test_task_list_renders_mobile_nav(self):
        response = self.client.get("/tasks/")
        self.assertContains(response, "md:hidden")

    def test_login_page_renders_dark(self):
        self.client.logout()
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "bg-slate-950")
