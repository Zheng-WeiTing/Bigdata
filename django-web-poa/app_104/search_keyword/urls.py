from django.urls import path
from . import views

app_name="search_keyword"

urlpatterns = [
    
    path('', views.home, name='home'),
    path('api_get_top_userkey/', views.api_get_top_userkey, name='api_get_top_userkey'),


]
