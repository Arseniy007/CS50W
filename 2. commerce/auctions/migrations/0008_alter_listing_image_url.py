# Generated by Django 4.2.3 on 2023-07-19 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listing_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image_url',
            field=models.CharField(blank=True, default='https://www.google.com/url?sa=i&url=https%3A%2F%2Fdepositphotos.com%2F121012076%2Fstock-illustration-blank-photo-icon.html&psig=AOvVaw2T-Gv7Po4E5-m41KaqVdP5&ust=1689846253440000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCJCB_v69moADFQAAAAAdAAAAABAw', max_length=100),
        ),
    ]
