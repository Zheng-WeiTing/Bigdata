from django.urls import path
from . import views

app_name = 'conditional_analysis'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/conditional/', views.conditional_analysis, name='conditional_analysis_api'),
]