from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import get_object_or_404, redirect
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import LoginSerializer, PostSerializer, SignUpSerializer

User = get_user_model()


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=["get"],
        detail=True,
        url_path="like",
        url_name="like",
        permission_classes=[permissions.IsAuthenticated],
    )
    def like(self, request, pk=None, *args, **kwargs):
        """
        Отправьте GET чтобы like пост
        """
        if request.method == "GET":
            post = get_object_or_404(Post, pk=pk)
            post.likes += 1
            post.save()
            return redirect(f'/posts/{pk}/')
        return None

    @action(
        methods=["get"],
        detail=True,
        url_path="unlike",
        url_name="unlike",
        permission_classes=[permissions.IsAuthenticated],
    )
    def unlike(self, request, pk=None, *args, **kwargs):
        """
        Отправьте GET чтобы unlike пост
        """
        if request.method == "GET":
            post = get_object_or_404(Post, pk=pk)
            post.likes -= 1
            post.save()
            return redirect(f'/posts/{pk}/')
        return None


class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Отправьте POST для создания пользователя
        {
            "username": "string",
            "password": "string"
        }
        """
        serializer = SignUpSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        username = serializer.validated_data.get("username")
        if User.objects.filter(username=username).exists():
            return Response(
                "Такой username уже зарегистрирован",
                status=status.HTTP_200_OK,
            )

        password = serializer.validated_data.get("password")
        user = User.objects.create(
            username=str(username),
        )
        user.set_password(password)
        user.save()

        return Response(request.data, status=status.HTTP_200_OK)

    def get(self, request):
        """
        Отправьте POST для создания пользователя
        {
            "username": "string",
            "password": "string"
        }
        """
        serializer = SignUpSerializer()
        return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
        )


class MyLoginView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Отправьте POST для логина пользователя
        {
            "username": "string",
            "password": "string"
        }
        """
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(
                f"{username} успешно залогинился",
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                "Такой username не зарегистрирован",
                status=status.HTTP_200_OK,
            )

    def get(self, request):
        """
        Отправьте POST для логина пользователя
        {
            "username": "string",
            "password": "string"
        }
        """
        serializer = LoginSerializer()
        return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
        )
