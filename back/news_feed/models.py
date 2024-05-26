from django.db import models

# Create your models here.

class News(models.Model):
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
    groq_question_3 = models.CharField(max_length=1000, blank=True)

    image_cover = models.URLField(max_length=1000, blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True)

    news_source = models.URLField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.groq_title

