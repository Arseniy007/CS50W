# Generated by Django 4.2.3 on 2023-07-19 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_remove_watchlist_listing_watchlist_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='listing',
            field=models.ManyToManyField(blank=True, related_name='listings', to='auctions.listing'),
        ),
    ]