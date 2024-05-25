from rest_framework import generics

from .models import News
from .serializers import NewsSerializer


class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.order_by('-base_date')
    serializer_class = NewsSerializer
