from django.test import TestCase
from django.urls import reverse

from main import models


class IndexTestCase(TestCase):
    def test_index(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)


class BlogCreateTestCase(TestCase):
    def test_blog_creation(self):
        data = {
            "title": "jon's blog",
            "url": "https://jon.com",
            "description": "opinions",
        }
        response = self.client.post(reverse("blog_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(models.Blog.objects.get(url=data["url"]))
