# Generated by Django 4.2.3 on 2023-07-21 09:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_comment_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
