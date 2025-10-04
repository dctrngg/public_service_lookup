# feedback/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_feedback, name='submit_feedback'),
    path('success/<str:tracking_code>/', views.feedback_success, name='feedback_success'),
    path('track/', views.track_feedback, name='track_feedback'),
    path('list/', views.feedback_list, name='feedback_list'),
]