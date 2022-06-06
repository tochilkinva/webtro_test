# Generated by Django 3.2.13 on 2022-06-06 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_postuserlike'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postuserlike',
            name='like',
            field=models.IntegerField(choices=[(1, 'Like'), (-1, 'Unlike'), (0, 'Neutral')], default=0, verbose_name='Одобрение поста пользователем'),
        ),
    ]