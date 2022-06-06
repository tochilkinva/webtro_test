from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import get_object_or_404, redirect
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import LikeStatus, Post, PostUserLike
from .serializers import LoginSerializer, PostSerializer, SignUpSerializer

User = get_user_model()


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
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
        methods=["post"],
        detail=True,
        url_path="like",
        url_name="like",
        permission_classes=[permissions.IsAuthenticated],
    )
    def like(self, request, pk=None, *args, **kwargs):
        """
        Отправьте POST чтобы like пост
        """
        if request.method == "POST":
            post = get_object_or_404(Post, pk=pk)
            user = request.user
            # проверить есть ли оценка от него
            # если нет создать положительную и добавить лайк в пост и выйти
            if not PostUserLike.objects.filter(user=user, post=post,).exists():
                post_user_like = PostUserLike.objects.create(
                    user=user,
                    post=post,
                    like=LikeStatus.LIKE
                )
                post_user_like.save()
                post.likes += 1
                post.save()
                return Response(
                    f"{user} поставил Like посту: {post}",
                    status=status.HTTP_200_OK,
                )

            post_user_like = PostUserLike.objects.get(user=user, post=post,)
            # если нейтральная перевести в положительную
            if post_user_like.like == LikeStatus.NEUTRAL:
                post_user_like.like = LikeStatus.LIKE
                post_user_like.save()
                post.likes += 1
                post.save()
                return redirect(f'/posts/{pk}/')

            # если положительная перевести на нейтральную
            if post_user_like.like == LikeStatus.LIKE:
                post.likes -= 1
                post_user_like.like = LikeStatus.NEUTRAL
            # если отрицательная перевести на положительную
            else:
                post.likes += 2
                post_user_like.like = LikeStatus.LIKE
            post_user_like.save()
            post.save()
            return redirect(f'/posts/{pk}/')

        return Response(
            "Метод не реализован",
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    @action(
        methods=["post"],
        detail=True,
        url_path="unlike",
        url_name="unlike",
        permission_classes=[permissions.IsAuthenticated],
    )
    def unlike(self, request, pk=None, *args, **kwargs):
        """
        Отправьте POST чтобы unlike пост
        """
        if request.method == "POST":
            post = get_object_or_404(Post, pk=pk)
            user = request.user
            # проверить есть ли оценка от него
            # если нет создать положительную и добавить лайк в пост и выйти
            if not PostUserLike.objects.filter(user=user, post=post,).exists():
                post_user_like = PostUserLike.objects.create(
                    user=user,
                    post=post,
                    like=LikeStatus.LIKE
                )
                post_user_like.save()
                post.likes -= 1
                post.save()
                return Response(
                    f"{user} поставил Unlike посту: {post}",
                    status=status.HTTP_200_OK,
                )

            post_user_like = PostUserLike.objects.get(user=user, post=post,)
            # если нейтральная перевести в отрицательную
            if post_user_like.like == LikeStatus.NEUTRAL:
                post_user_like.like = LikeStatus.UNLIKE
                post_user_like.save()
                post.likes -= 1
                post.save()
                return redirect(f'/posts/{pk}/')

            # если положительная перевести на отрицательную
            if post_user_like.like == LikeStatus.LIKE:
                post.likes -= 2
                post_user_like.like = LikeStatus.UNLIKE
            # если отрицательная перевести на нейтральную
            else:
                post.likes += 1
                post_user_like.like = LikeStatus.NEUTRAL
            post_user_like.save()
            post.save()
            return redirect(f'/posts/{pk}/')

        return Response(
            "Метод не реализован",
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


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
