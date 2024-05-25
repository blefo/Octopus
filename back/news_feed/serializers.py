from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            "date_added",
            "groq_title",
            "groq_key_point_1",
            "groq_key_point_2",
            "groq_key_point_3",
            "groq_question_1",
            "groq_question_2",
        ]