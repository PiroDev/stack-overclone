from django.urls import path
from .views import *

urlpatterns = [
    path('', index_view, name='index'),
    path('hot/', hot_questions_view, name='hot_questions'),
    path('tag/<str:tag>', questions_by_tag_view, name='questions_by_tag'),
    path('<int:question_id>/', question_and_answers_view, name='question_and_answers'),
    path('ask/', ask_question_view, name='ask_question'),
]
