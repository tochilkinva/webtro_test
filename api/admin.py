from django.contrib import admin

from .models import Post, PostUserLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "likes", "pub_date")
    empty_value_display = "-пусто-"


@admin.register(PostUserLike)
class PostUserLikeAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "like")
    empty_value_display = "-пусто-"
