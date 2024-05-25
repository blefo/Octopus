from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics

from .models import News
from .serializers import NewsSerializer


class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [
        OrderingFilter,
        SearchFilter,
    ]
    search_fields = ['groq_title']
    ordering =['-base_date']



