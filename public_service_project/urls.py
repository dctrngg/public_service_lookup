"""
URL configuration for public_service_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.views.generic import TemplateView

from services.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('services/', include('services.urls')),
    path("feedback/", include("feedback.urls")),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]

# Tùy chỉnh tiêu đề Admin
admin.site.site_header = 'Quản trị Dịch vụ Hành chính Công'
admin.site.site_title = 'Admin DVHCC'
admin.site.index_title = 'Quản lý Hệ thống'