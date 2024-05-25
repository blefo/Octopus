from django.urls import path
from .views import GenerateFollowUpContent
urlpatterns = [
    path("follow/", GenerateFollowUpContent.as_view(), name="next_move_followup"),
]