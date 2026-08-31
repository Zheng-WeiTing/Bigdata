from django.urls import path
from . import views

app_name = 'tool_analysis'

urlpatterns = [
    path('', views.home, name='home'),
    path('get_wordcloud_data/<str:job_type>/', views.get_wordcloud_data, name='get_wordcloud_data'),
    path('get_bubble_data/', views.get_bubble_data, name='get_bubble_data'),
]