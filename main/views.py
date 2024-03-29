import random
import urllib.error
import urllib.request

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from main import models


class BlogList(ListView):
    template_name = "main/index.html"

    def get_queryset(self):
        class KeywordForm(forms.Form):
            key = forms.CharField(max_length=50)

        form = KeywordForm(self.request.GET)
        if form.is_valid():
            return models.Blog.objects.filter(
                description__icontains=form.cleaned_data["key"]
            ).order_by("?")
        else:
            return models.Blog.objects.all().order_by("?")


class BlogCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = models.Blog
    fields = ["title", "url", "description"]
    success_url = reverse_lazy("index")
    success_message = "addition of %(url)s successful"

    def form_valid(self, form):
        form.cleaned_data["title"] = form.cleaned_data["title"].strip()
        form.cleaned_data["url"] = form.cleaned_data["url"].strip()
        form.cleaned_data["description"] = form.cleaned_data["description"].strip()
        return super().form_valid(form)


@require_POST
def metadata(request):
    class MetadataForm(forms.Form):
        url = forms.URLField()

    form = MetadataForm(request.POST)
    if form.is_valid():
        try:
            webpage = urllib.request.urlopen(form.cleaned_data.get("url")).read()
            webpage = str(webpage).replace("\n", " ")

            if "<title>" not in webpage:
                return HttpResponse("no title")

            title = webpage.split("<title>")[1].split("</title>")[0]
        except (urllib.error.HTTPError, urllib.error.URLError):
            title = ""
        return HttpResponse(title)
    else:
        return HttpResponse("invalid")


def go_random(request):
    all_blogs = models.Blog.objects.all()
    random_blog = random.choice(all_blogs)
    return redirect(random_blog.url)
