from django import forms

class QuestionForm(forms.Form):
    CHOICES = (('a','a'),
               ('b','b'),
               ('c','c'),
               ('d','d'),)
    chosen = forms.MultipleChoiceField(choices=CHOICES, widget=forms.MultipleChoiceField)