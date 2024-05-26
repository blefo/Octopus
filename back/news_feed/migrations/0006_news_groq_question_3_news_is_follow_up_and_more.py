# Generated by Django 5.0.6 on 2024-05-26 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_feed', '0005_news_image_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='groq_question_3',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='news',
            name='is_follow_up',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='news',
            name='news_source',
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
    ]
