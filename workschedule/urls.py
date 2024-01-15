from django.contrib import admin
from django.urls import path
from. import views

urlpatterns = [
    path('home/',  views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('personalinfo_input/', views.personalinfo_input, name='personalinfo_input'),
    path('surveyCalendar/', views.surveyCalendar_view, name='surveyCalendar'),
    path('schedule_data/', views.schedule_data, name='schedule_data'), 
    path('definition/', views.definition_view, name='definition'),     
]
