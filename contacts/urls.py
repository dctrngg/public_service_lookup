# contacts/urls.py

from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.contact_list, name='contact_list'),
    path('phong-ban/<int:pk>/', views.department_detail, name='department_detail'),
    path('khan-cap/', views.emergency_list, name='emergency_list'),
]