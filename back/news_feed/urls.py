from django.urls import path
from .views import NewsListAPIView, CallFucntionsAPIView

urlpatterns = [
    path('news/', NewsListAPIView.as_view(), name='news_list'),
    path("genereate/", CallFucntionsAPIView.as_view())
]