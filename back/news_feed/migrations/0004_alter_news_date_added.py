# Generated by Django 5.0.6 on 2024-05-25 15:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("news_feed", "0003_news_base_date_news_date_added"),
    ]

    operations = [
        migrations.AlterField(
            model_name="news",
            name="date_added",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
