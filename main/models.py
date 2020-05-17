from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=500)
    url = models.URLField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
