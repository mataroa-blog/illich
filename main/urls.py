from django.contrib import admin
from django.urls import path

from main import views

admin.site.site_header = "illich administration"

urlpatterns = [
    path("", views.BlogListView.as_view(), name="index"),
]
