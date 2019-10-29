from django.urls import path

from . import views

app_name = 'evaluation'
urlpatterns = [
    # /evaluation/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /evaluation/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex: /evaluation/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # ex: /evaluation/5/submit/
    path('<int:evaluation_id>/submit/', views.submitAnswers, name='submit'),
]