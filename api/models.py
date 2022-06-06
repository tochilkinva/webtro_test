from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Текст поста'
    )

    likes = models.IntegerField(
        verbose_name='Количество лайков',
        default=0
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:20]


class LikeStatus(models.IntegerChoices):
    LIKE = 1
    UNLIKE = -1
    NEUTRAL = 0


class PostUserLike(models.Model):

    like = models.IntegerField(
        verbose_name='Одобрение поста пользователем',
        choices=LikeStatus.choices,
        default=LikeStatus.NEUTRAL
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='postuserlikes',
        verbose_name='Пост',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='postuserlikes',
        verbose_name='Пользователь',
    )

    class Meta:
        ordering = ('user', 'post',)
        verbose_name = 'Одобрение поста'
        verbose_name_plural = 'Одобрение постов'

    def __str__(self):
        return f'{self.post} - {self.user}: {self.like}'
