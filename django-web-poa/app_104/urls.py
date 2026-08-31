from django.urls import path, include
from . import views

app_name = 'app_104'

urlpatterns = [
    path('', views.home, name='home'),
    path('area_analysis/', include(('app_104.area_analysis.urls', 'area_analysis'), namespace='area_analysis')),
    path('tool_analysis/', include(('app_104.tool_analysis.urls', 'tool_analysis'), namespace='tool_analysis')),
    path('salary_analysis/', include(('app_104.salary_analysis.urls', 'salary_analysis'), namespace='salary_analysis')),
    path('conditional_analysis/', include(('app_104.conditional_analysis.urls', 'conditional_analysis'), namespace='conditional_analysis')),
    path('search_keyword/', include(('app_104.search_keyword.urls', 'search_keyword'), namespace='search_keyword')),
    path('trait_analysis/', include(('app_104.trait_analysis.urls', 'trait_analysis'), namespace='trait_analysis')),
    path('top_keyword/', include(('app_104.top_keyword.urls', 'top_keyword'), namespace='top_keyword')),
    
]