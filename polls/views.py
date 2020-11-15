from django.shortcuts import render,get_object_or_404
#from django.template import loader
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
#from django.http import Http404
from .models import Question,Choice
from django.views import generic
from django.urls import reverse


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

# def IndexView(generic.ListView):
#     latest_question_list=Question.objects.order_by('pub_date')[:5]
#     #template=loader.get_template('polls/index.html')
#     context={'latest_question_list':latest_question_list,
#     }
#     return render(request,'polls/index.html',context)#HttpResponse(template.render(context,request))

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'


# def detail(request,question_id):
#     question_details=get_object_or_404(Question, pk=question_id)
#     return render(request,"polls/details.html",{'question':question_details,})

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# def results(request,question_id):
#     question_details=get_object_or_404(Question, pk=question_id)
#     return render(request,"polls/results.html",{'question':question_details,})

def vote(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/details.html',{
            'question':question,
            'error_message':"You didn't select a choice.",
            })
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))



def owner(request):
    return HttpResponse("Hello, world. bc29e1f1 is the polls index.")