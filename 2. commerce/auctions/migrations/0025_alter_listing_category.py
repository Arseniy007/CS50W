# Generated by Django 4.2.3 on 2023-07-23 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0024_comment_headline_alter_listing_start_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='listings', to='auctions.category'),
        ),
    ]