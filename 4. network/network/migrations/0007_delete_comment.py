# Generated by Django 4.2.3 on 2023-08-11 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_alter_post_text_comment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]