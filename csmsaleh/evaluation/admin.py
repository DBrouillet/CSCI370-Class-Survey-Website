from django.contrib import admin

from .models import Evaluation, Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 5

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
    fieldsets = [
        (None, {'fields': ['question_text']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Evaluation, EvaluationAdmin)

