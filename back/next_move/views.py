from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from news_feed.llm_manager.inference_structure import GroqNews
from news_feed.models import News
from news_feed.serializers import NewsSerializer

from .pipeline_bis import generate_follow_up_question

from rest_framework import serializers
class FollowUpQuestionSerializer(serializers.Serializer):
    question = serializers.CharField()
# Create your views here.
import asyncio
class GenerateFollowUpContent(APIView):
    serializer_class = FollowUpQuestionSerializer
    def post(self, request):
        question = str(request.data['question'])

        next_content: GroqNews = asyncio.run(generate_follow_up_question(question))

        groq_follow_up = News.objects.create(
             hash=str(hash(next_content["rephrased_title"])),
             base_title=next_content["rephrased_title"],
             base_content=next_content["rephrased_title"],
             groq_title=next_content["rephrased_title"],
             groq_key_point_1=next_content["news_keypoints"][0],
             groq_key_point_2=next_content["news_keypoints"][1],
             groq_key_point_3=next_content["news_keypoints"][2],
             groq_question_1=next_content["news_related_question"][0],
             groq_question_2=next_content["news_related_question"][1],
             groq_question_3=next_content["news_related_question"][2],
             image_cover="",
             is_follow_up=True
         )

        serialized = NewsSerializer(groq_follow_up)
        return Response(serialized.data)





