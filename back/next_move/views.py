from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

#from news_feed.llm_manager.inference_structure import GroqNews

from news_feed.models import News
from news_feed.serializers import NewsSerializer

#from .pipeline_bis import generate_follow_up_question
from octopus_lib.pipelines.respond_question import generate_follow_up_question
from octopus_lib.model_config.instructor import GroqNews

from rest_framework import serializers

import asyncio


class FollowUpQuestionSerializer(serializers.Serializer):
    question = serializers.CharField()
# Create your views here.

class GenerateFollowUpContent(APIView):
    serializer_class = FollowUpQuestionSerializer
    def post(self, request):
        print(f"request.data: {request.data}")
        question = str(request.data['question'])
        title_previous_news = str(request.data['previous_news']['groq_title'])
        key_points_previous_news = [str(request.data['previous_news']['groq_key_point_1']), str(request.data['previous_news']['groq_key_point_2']), str(request.data['previous_news']['groq_key_point_3'])]

        next_content: GroqNews = asyncio.run(generate_follow_up_question(question, title_previous_news, key_points_previous_news))
        print(f"Next content: {next_content}")
        
        # verify number of keypoints
        if len(next_content["news_keypoints"]) < 3:
            next_content["news_keypoints"] += [""] * (3 - len(next_content["news_keypoints"]))
        # verify number of questions
        if len(next_content["news_related_question"]) < 3:
            next_content["news_related_question"] += [""] * (3 - len(next_content["news_related_question"]))
        

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

        serialized = NewsSerializer(groq_follow_up).data
        serialized["sources"] = next_content["sources"]
        return Response(serialized)





