import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group


class Evaluation(models.Model):
    eval_text = models.CharField('Evaluation Title', max_length=200) #Evaluation name as seen by the user
    pub_date = models.DateTimeField('publish date')
    # eval_group = models.ForeignKey(Group)
    def __str__(self):
        return self.eval_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= self.pub_date <= now # number of days to show recent evals for
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Visible to Users'



class Question(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    # is_required = models.BooleanField(default=True)
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    def __str__(self):
        return self.choice_text

class UserAnswers(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    submitTime = models.DateField(auto_now=True)
    userName = models.CharField(max_length=30)