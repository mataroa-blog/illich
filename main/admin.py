from django.contrib import admin

from main import models


class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "url")


admin.site.register(models.Blog, BlogAdmin)
