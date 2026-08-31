from django.urls import path
from . import views

app_name = 'trait_analysis'

urlpatterns = [
    path('', views.home, name='home'),
    path('get_traits_data/', views.get_traits_data, name='get_traits_data'),
]