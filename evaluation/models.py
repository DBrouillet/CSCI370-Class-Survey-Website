import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group



class FreeResponseQuestion(models.Model):
    question_text = models.CharField(max_length=200)
    def __str__(self):
        return self.question_text

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    def __str__(self):
        return self.question_text

class Evaluation(models.Model):
    eval_text = models.CharField('Evaluation Title', max_length=200) #Evaluation name as seen by the user
    pub_date = models.DateTimeField('publish date')
    #Attaching groups and questions to the Evaluation model in ManyToMany format to allow for reuse of those models
    groups = models.ManyToManyField(Group)
    freeResponseQuestions = models.ManyToManyField(FreeResponseQuestion)
    questions = models.ManyToManyField(Question)
    def __str__(self):
        return self.eval_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= self.pub_date <= now # number of days to show recent evals for
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    # Message seen on admin site for recently published evals
    was_published_recently.short_description = 'Visible to Users'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    def __str__(self):
        return self.choice_text

class FreeResponseAnswer(models.Model):
    answerText = models.CharField(max_length=1000, default=None, blank=True, null=True)

class UserAnswers(models.Model):
    #UserAnswers contain fields for every other model in order to save all relevant information for CSV files
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, default=None, blank=True, null=True)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, default=None, blank=True, null=True)
    freeResponseQuestion = models.ForeignKey(FreeResponseQuestion, on_delete=models.CASCADE, default=None, blank=True, null=True)
    freeResponseAnswer = models.ForeignKey(FreeResponseAnswer, on_delete=models.CASCADE, default=None, blank=True, null=True)
    submitTime = models.DateField(auto_now=True)
    userName = models.CharField(max_length=30)
    firstName = models.CharField(max_length=30, blank=True, null=True)
    lastName = models.CharField(max_length=30, blank=True, null=True)