from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice

# Create your views here.
def index(request):
    '''显示欢迎页'''
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list':latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    '''显示投票问题详细页'''
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question':question})

def vote(request, question_id):
    '''投票问题的选项'''
    question = get_object_or_404(Question, pk=question_id)
    try:
        select_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question':question,
            'error_message':'点选后才能提交',
        })
    else:
        select_choice.votes += 1
        select_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def results(request, question_id):
    '''投票结果页'''
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})