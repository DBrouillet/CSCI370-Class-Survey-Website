import csv
from django.shortcuts import get_object_or_404, render, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import Group
from .models import Evaluation, Choice, Question, UserAnswers, FreeResponseAnswer, FreeResponseQuestion


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'evaluation/index.html'
    context_object_name = 'latest_evaluation_list'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Evaluation.objects.filter(
            pub_date__lte=timezone.now(), pub_date__gte=datetime.now()-timedelta(days=7),

        ).order_by('-pub_date')


class DetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Evaluation
    template_name = 'evaluation/detail.html'



class ResultsView(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Evaluation
    template_name = 'evaluation/results.html'

def submitAnswers(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, pk=evaluation_id)
    choices = []
    i = 0
    #iterates through all questions to see if they were answered
    # currently, data returned by the POST is numerical, not very useful
    for c in evaluation.question_set.all():
        try:
            # using i and questNum as temp variables to iterate through user selections
            i = i + 1
            quest_num = "choice" + str(i)
            data = request.POST.copy()
            answer = data.get(quest_num)
            final_choice = Choice.objects.get(id = answer) #taking the cleaned POST data and retrieving the corresponding choice to save
            choiceType = "C"
            choices.append([final_choice, choiceType])
        except:
            return render(request, 'evaluation/detail.html', {
                        'evaluation': evaluation,
                        'error_message': "You did not answer one of the required questions.",
                    })

    i = 0
    for c in evaluation.freeresponsequestion_set.all():
        i = i + 1
        name = "textarea" + str(i)
        data = request.POST.copy()
        answer = data.get(name)
        if answer != '':
            
            choices.append([])

    for ch in choices:
        if ch[1] == "C":
            new_answer = UserAnswers(choice=ch[0], userName=request.user)
        else:
            new_answer = UserAnswers(freeResponseAnswer=ch[0], FreeResponseQuestion=ch, userName=request.user)
        new_answer.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    # This line sends the user to the results.html page
    return HttpResponseRedirect(reverse('evaluation:results', args=(evaluation.id,)))