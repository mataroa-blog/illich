import random

from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from main import models


class BlogList(ListView):
    template_name = "main/index.html"
    queryset = models.Blog.objects.all().order_by("?")


class BlogCreate(SuccessMessageMixin, CreateView):
    model = models.Blog
    fields = ["title", "url", "description"]
    success_url = reverse_lazy("index")
    success_message = "addition of %(url)s successful"

    def form_valid(self, form):
        form.cleaned_data["title"] = form.cleaned_data["title"].strip()
        form.cleaned_data["url"] = form.cleaned_data["url"].strip()
        form.cleaned_data["description"] = form.cleaned_data["description"].strip()
        return super().form_valid(form)


def go_random(request):
    all_blogs = models.Blog.objects.all()
    random_blog = random.choice(all_blogs)
    return redirect(random_blog.url)
