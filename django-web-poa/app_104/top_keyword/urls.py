from django.urls import path
from . import views

app_name = 'top_keyword'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/keywords/', views.get_keywords, name='get_keywords'),

]