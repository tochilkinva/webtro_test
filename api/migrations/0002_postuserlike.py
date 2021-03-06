# Generated by Django 3.2.13 on 2022-06-06 15:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostUserLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.IntegerField(choices=[(1, 'like'), (-1, 'unlike'), (0, 'neutral')], default=0, verbose_name='Одобрение поста пользователем')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postuserlikes', to='api.post', verbose_name='Пост')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postuserlikes', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Одобрение поста',
                'verbose_name_plural': 'Одобрение постов',
                'ordering': ('user', 'post'),
            },
        ),
    ]
