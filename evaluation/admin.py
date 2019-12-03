from django.contrib import admin
import csv
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.admin import GroupAdmin
from django.shortcuts import get_object_or_404, render, HttpResponse
from .models import Evaluation, Question, Choice, UserAnswers, FreeResponseQuestion, FreeResponseAnswer



class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class FreeResponseInline(admin.TabularInline):
    model = FreeResponseQuestion
    extra = 0

class EvaluationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['eval_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [QuestionInline, FreeResponseInline]
    list_display = ('eval_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['eval_text']

class FreeResponseQuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['question_text']}),
    ]

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['question_text']}),
    ]
    inlines = [ChoiceInline]

class GroupsAdmin(GroupAdmin):
    list_display = ["name"]
    actions = ['download_csv']

    # Tutorial at https://www.youtube.com/watch?v=cYsU1pUzu4o

    def download_csv(self, request, queryset):
        items = UserAnswers.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Recorded Responses.csv"'
        writer = csv.writer(response, delimiter=',')
        writer.writerow(['Evaluation Name', 'User Name', 'Question', 'Answer', 'Evaluation Publish Date', 'Submit Date'])
        for obj in items:
            for group in queryset:
                if User.objects.filter(username=obj.userName, groups__name=group).exists():
                    if obj.choice is not None:
                        writer.writerow([obj.choice.question.evaluation.eval_text, obj.userName, obj.choice.question, obj.choice, obj.choice.question.evaluation.pub_date, obj.submitTime])
                    elif obj.freeResponseQuestion is not None and obj.freeResponseAnswer is not None:
                        writer.writerow([obj.freeResponseQuestion.evaluation.eval_text, obj.userName, obj.freeResponseQuestion.question_text, obj.freeResponseAnswer.answerText, obj.freeResponseQuestion.evaluation.pub_date, obj.submitTime])
        return response

admin.site.unregister(Group)
admin.site.register(Group, GroupsAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Evaluation, EvaluationAdmin)


