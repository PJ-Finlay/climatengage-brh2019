from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reps/', views.reps, name='reps'),
    path('about/', views.about, name='about')
]