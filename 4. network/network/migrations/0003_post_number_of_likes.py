# Generated by Django 4.2.3 on 2023-08-08 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_remove_like_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='number_of_likes',
            field=models.IntegerField(default=0),
        ),
    ]
