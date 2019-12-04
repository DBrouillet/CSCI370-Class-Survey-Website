from django.contrib import admin
import csv
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.admin import GroupAdmin
from django.shortcuts import get_object_or_404, render, HttpResponse
from .models import Evaluation, Question, Choice, UserAnswers, FreeResponseQuestion, FreeResponseAnswer

#Creating inlines for choices, Questions, FreeResponseQuestions, and Groups
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionInline(admin.TabularInline):
    model = Evaluation.questions.through
    verbose_name = "Question"
    verbose_name_plural = "Questions"
    extra = 0

class FreeResponseInline(admin.TabularInline):
    model = Evaluation.freeResponseQuestions.through
    verbose_name = "Free Response Question"
    verbose_name_plural = "Free Response Questions"
    extra = 0

class GroupsInline(admin.TabularInline):
    model = Evaluation.groups.through
    verbose_name = "Group"
    verbose_name_plural = "Assigned Groups"
    extra = 0

#Creating custom admin fields for administrators to edit various fields when creating evaluations
class EvaluationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['eval_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [GroupsInline, QuestionInline, FreeResponseInline]
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

    # This is the function we use to download csvs
    # Tutorial we used to create it was found at https://www.youtube.com/watch?v=cYsU1pUzu4o (sometime in October 2019)
    def download_csv(self, request, queryset):
        items = UserAnswers.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Recorded Responses.csv"'
        writer = csv.writer(response, delimiter=',')
        #Writing the top line with column names
        writer.writerow(['Evaluation Name', 'User Name', 'First Name', 'Last Name', 'Question', 'Answer', 'Evaluation Publish Date', 'Submit Date'])
        for obj in items:
            for group in queryset:
                #filtering responses to only output for the selected groups
                if User.objects.filter(username=obj.userName, groups__name=group).exists():
                    if obj.choice is not None:
                        writer.writerow([obj.evaluation.eval_text, obj.userName, obj.firstName, obj.lastName, obj.choice.question, obj.choice, obj.evaluation.pub_date, obj.submitTime])
                    elif obj.freeResponseQuestion is not None and obj.freeResponseAnswer is not None:
                        writer.writerow([obj.evaluation.eval_text, obj.userName, obj.firstName, obj.lastName, obj.freeResponseQuestion.question_text, obj.freeResponseAnswer.answerText, obj.evaluation.pub_date, obj.submitTime])
        return response

#Unregistering the default Group behavior, then registering all custom administration views
admin.site.unregister(Group)
admin.site.register(Group, GroupsAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(FreeResponseQuestion)