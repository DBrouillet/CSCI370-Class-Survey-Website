from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Evaluation, Choice, Question

class IndexView(generic.ListView):
    template_name = 'evaluation/index.html'
    context_object_name = 'latest_evaluation_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Evaluation.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Evaluation
    template_name = 'evaluation/detail.html'


class ResultsView(generic.DetailView):
    model = Evaluation
    template_name = 'evaluation/results.html'

def submitAnswers(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, pk=evaluation_id)
    choices = []
    for choice in evaluation.question_set.all():
        try:
            choices.append(choice.get(pk=request.POST['choice']))
        except:
            return render(request, 'evaluation/detail.html', {
                    'evaluation': evaluation,
                    'error_message': "You did not answer one of the required questions.",
                })
    # for answer in choices:
    #    .save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('evaluation:results', args=(evaluation.id,)))
