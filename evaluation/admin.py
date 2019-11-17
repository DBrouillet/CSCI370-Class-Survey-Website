from django.contrib import admin
import csv
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from django.shortcuts import get_object_or_404, render, HttpResponse
from .models import Evaluation, Question, Choice, UserAnswers



class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class EvaluationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['eval_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [QuestionInline]
    list_display = ('eval_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['eval_text']
class QuestionAdmin(admin.ModelAdmin):
    list_select_related = [
        'evaluation',
    ]
    fieldsets = [
        (None, {'fields': ['question_text']}),
    ]
    inlines = [ChoiceInline]

class GroupsAdmin(GroupAdmin):
    list_display = ["name"]
    actions = ['download_csv']
    # This is how to download csvs. Go to /evaluation/download-csv to get it.
    # Tutorial at https://www.youtube.com/watch?v=cYsU1pUzu4o
    def download_csv(self, request, queryset):
        items = UserAnswers.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Recorded Responses.csv"'
        writer = csv.writer(response, delimiter=',')
        writer.writerow(['Evaluation Name', 'User Name', 'Question', 'Answer', 'Evaluation Publish Date', 'Submit Date'])
        for obj in items:
            writer.writerow([obj.choice.question.evaluation.eval_text, obj.userName, obj.choice.question, obj.choice,
                             obj.choice.question.evaluation.pub_date, obj.submitTime])
        return response
        # response = HttpResponse(content_type='text/csv')
        # response['Content-Disposition'] = 'attachment; filename="useranswers.csv"'
        # writer = csv.writer(response, delimiter=',')
        # writer.writerow(
        #     ['Evaluation Name', 'User Name', 'User Group' 'Evaluation Publish Date', 'Date Submitted', 'Question',
        #      'Answer'])
        # for g in Group.objects.all():
        #     items = UserAnswers.userName.groups.filter(name=g)
        #     for obj in items:
        #         writer.writerow([obj.choice.question.evaluation.eval_text, obj.userName, obj.userName.group,
        #                          obj.choice.question.evaluation.pub_date, obj.choice.question.evaluation_id,
        #                          obj.choice.question.question_text, obj.choice])
        # return response

admin.site.unregister(Group)
admin.site.register(Group, GroupsAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Evaluation, EvaluationAdmin)


