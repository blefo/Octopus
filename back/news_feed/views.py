from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import News
from .serializers import NewsSerializer
from .news_fetcher import news_generator

class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [
        OrderingFilter,
        SearchFilter,
    ]
    search_fields = ['groq_title']
    ordering =['-base_date']

class CallFucntionsAPIView(APIView):
    def get(self, request):
        news_generator()
        return Response("Hello")


