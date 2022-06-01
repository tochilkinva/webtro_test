from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("__all__")
        read_only_fields = ('likes', 'author')


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
    )
    password = serializers.CharField(
        required=True,
    )
