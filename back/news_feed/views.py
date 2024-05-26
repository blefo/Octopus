from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import News
from .serializers import NewsSerializer
#from .news_fetcher import news_generator
from octopus_lib.pipelines.news_fetcher import news_generator

class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.filter(is_follow_up=False)
    serializer_class = NewsSerializer
    filter_backends = [
        OrderingFilter,
        SearchFilter,
    ]
    search_fields = ['groq_title']
    ordering =['-date_added']

class CallFucntionsAPIView(APIView):
    def get(self, request):
        news_generator(News)
        return Response("Hello")


