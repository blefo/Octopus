# Generated by Django 5.0.6 on 2024-05-25 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_feed', '0004_alter_news_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='image_cover',
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
    ]