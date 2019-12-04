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

#Creating behavior for the various views. The LoginRequiredMixin ensures users are logged in in order to see pages
class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'evaluation/index.html'
    context_object_name = 'latest_evaluation_list'
    def get_queryset(self):
        #Return a list of any evaluations published within the last seven days, but not in the future
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
    for c in evaluation.questions.all():
        try:
            # using i and questNum as temp variables to iterate through user selections
            i = i + 1
            quest_num = "choice" + str(i)
            data = request.POST.copy()
            answer = data.get(quest_num)
            final_choice = Choice.objects.get(id = answer) #taking the cleaned POST data and retrieving the corresponding choice to save
            choiceType = "C"
            choices.append([evaluation, final_choice, choiceType])
        except:
            #return the user to the current page if they didn't answer a multiple choice question
            return render(request, 'evaluation/detail.html', {
                        'evaluation': evaluation,
                        'error_message': "You did not answer one of the required questions.",
                    })

    i = 0 #resetting the counter to iterate over free response questions
    for c in evaluation.freeResponseQuestions.all():
        i = i + 1
        name = "textarea" + str(i)
        data = request.POST.copy()
        answer = data.get(name)
        question = FreeResponseQuestion.objects.get(id = c.id)
        if answer != '':
            choices.append([evaluation, answer , question])
    #Sending the data to a UserAnswers object so admins can download a CSV of responses
    for ch in choices:
        if ch[2] == "C":
            new_answer = UserAnswers(evaluation=ch[0], choice=ch[1], userName=request.user, firstName=request.user.first_name, lastName=request.user.last_name)
        else:
            frAnswer = FreeResponseAnswer(answerText=ch[1])
            frAnswer.save()
            #UserAnswer saves the Evaluation object, any questions and their corresponding answers, as well as the user details
            new_answer = UserAnswers(evaluation=ch[0], freeResponseAnswer=frAnswer, freeResponseQuestion=ch[2], userName=request.user, firstName=request.user.first_name, lastName=request.user.last_name)
        new_answer.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    # This line sends the user to the results.html page
    return HttpResponseRedirect(reverse('evaluation:results', args=(evaluation.id,)))