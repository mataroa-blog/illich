from django.views.generic import ListView

from main import models


class BlogListView(ListView):
    template_name = "main/index.html"
    model = models.Blog
