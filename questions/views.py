from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Question
from stack_overclone.error_views import page_not_found_view

def index_view(request):
    query_set = Question.objects.get_new()
    page = paginate(query_set, request)
    data = {
        'questions': page.object_list,
        'page': page
    }
    return render(request, 'index.html', context=data)

def hot_questions_view(request):
    query_set = Question.objects.get_top_rated()
    page = paginate(query_set, request)
    data = {
        'questions': page.object_list,
        'page': page
    }
    return render(request, 'hot_questions.html', context=data)

def questions_by_tag_view(request, tag):
    query_set = Question.objects.get_by_tag(tag)
    if query_set.count() == 0:
        return page_not_found_view(request, 'No such tag')
    page = paginate(query_set, request)
    data = {
        'tag': tag,
        'questions': page.object_list,
        'page': page
    }
    return render(request, 'questions_by_tag.html', context=data)

def question_and_answers_view(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
    except Exception:
        return page_not_found_view(request, 'No such question')
    query_set = question.get_answers()
    page = paginate(query_set, request)
    data = {
        'question': question,
        'answers': page.object_list,
        'page': page
    }
    return render(request, 'question_and_answers.html', context=data)

def ask_question_view(request):
    return render(request, 'ask_question.html')

def paginate(query_set, request, per_page=20):
    paginator = Paginator(query_set, per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page

from django import template

register = template.Library()

@register.filter(name='add')
def add(value, arg):
    return int(value) + int(arg)
