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


class BlogCreateDuplicateTestCase(TestCase):
    def test_duplicate_blog_creation(self):
        data = {
            "title": "jon's blog",
            "url": "https://jon.com",
            "description": "opinions",
        }
        self.client.post(reverse("blog_create"), data)
        data = {
            "title": "jon's 2nd blog",
            "url": "https://jon.com",
            "description": "opinions",
        }
        response = self.client.post(reverse("blog_create"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Blog.objects.filter(url=data["url"]).count(), 1)


class MetadataTestCase(TestCase):
    def test_metadata_title(self):
        data = {
            "url": "https://sirodoht.com/",
        }
        response = self.client.post(reverse("metadata"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "sirodoht blog")

    def test_metadata_invalid_url(self):
        data = {
            "url": "this-is not a _URL_",
        }
        response = self.client.post(reverse("metadata"), data)
        self.assertEqual(response.status_code, 200)

    def test_metadata_not_found_url(self):
        data = {
            "url": "https://sirodoht.com/404",
        }
        response = self.client.post(reverse("metadata"), data)
        self.assertEqual(response.status_code, 200)
