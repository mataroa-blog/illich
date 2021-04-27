from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from main import models


class IndexTestCase(TestCase):
    def test_index(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)


class BlogCreateTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="alice")
        self.user.set_password("abcdef123456")
        self.user.save()
        self.client.login(username="alice", password="abcdef123456")

    def test_blog_creation(self):
        data = {
            "title": "alice's blog",
            "url": "https://alice.mataroa.blog",
            "description": "opinions",
        }
        response = self.client.post(reverse("blog_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(models.Blog.objects.get(url=data["url"]))


class BlogCreateDuplicateTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="alice")
        self.user.set_password("abcdef123456")
        self.user.save()
        self.client.login(username="alice", password="abcdef123456")

        data = {
            "title": "alice's blog",
            "url": "https://alice.mataroa.blog",
            "description": "opinions",
        }
        self.client.post(reverse("blog_create"), data)

    def test_duplicate_blog_creation(self):
        data = {
            "title": "alice's 2nd blog",
            "url": "https://alice.mataroa.blog",
            "description": "opinions",
        }
        response = self.client.post(reverse("blog_create"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Blog.objects.filter(url=data["url"]).count(), 1)


class MetadataTestCase(TestCase):
    def test_metadata_title(self):
        data = {
            "url": "https://mataroa.blog/",
        }
        response = self.client.post(reverse("metadata"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mataroa")

    def test_metadata_invalid_url(self):
        data = {
            "url": "this-is not a _URL_",
        }
        response = self.client.post(reverse("metadata"), data)
        self.assertEqual(response.status_code, 200)

    def test_metadata_not_found_url(self):
        data = {
            "url": "https://mataroa.blog/404",
        }
        response = self.client.post(reverse("metadata"), data)
        self.assertEqual(response.status_code, 200)
