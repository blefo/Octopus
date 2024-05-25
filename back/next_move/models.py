from django.db import models

# Create your models here.

class ArticleVector(models.Model):
    hash = models.CharField(max_length=400, unique=True)
    base_title = models.CharField(max_length=1000)
    base_content = models.TextField()
    base_date = models.DateField(null=True, blank=True)
    groq_title = models.CharField(max_length=1000, blank=True)

    groq_key_point_1 = models.CharField(max_length=1000, blank=True)
    groq_key_point_2 = models.CharField(max_length=1000, blank=True)
    groq_key_point_3 = models.CharField(max_length=1000, blank=True)

    groq_question_1 = models.CharField(max_length=1000, blank=True)
    groq_question_2 = models.CharField(max_length=1000, blank=True)

    date_added = models.DateField(auto_now_add=True)


