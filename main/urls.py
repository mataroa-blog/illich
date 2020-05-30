from django.contrib import admin
from django.urls import path

from main import views

admin.site.site_header = "illich administration"

urlpatterns = [
    path("", views.BlogList.as_view(), name="index"),
    path("new/", views.BlogCreate.as_view(), name="blog_create"),
    path("random/", views.go_random, name="go_random"),
]
