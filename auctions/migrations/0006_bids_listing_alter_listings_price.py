# Generated by Django 5.2.3 on 2025-06-20 20:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_bids_bid_bids_user_comments_author_comments_listing_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bids',
            name='listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listingbid', to='auctions.listings'),
        ),
        migrations.AlterField(
            model_name='listings',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
