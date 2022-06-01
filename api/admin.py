from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "likes", "pub_date")
    empty_value_display = "-пусто-"
