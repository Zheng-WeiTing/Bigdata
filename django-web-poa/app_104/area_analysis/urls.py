from django.urls import path
from . import views

app_name = 'area_analysis'

urlpatterns = [
    path('', views.home, name='home'),
    path('get_jobs/', views.get_jobs, name='get_jobs'),
]