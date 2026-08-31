from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    # top keywords
    path('topword/', include('app_top_keyword.urls')),
    
    # app top persons
    path('topperson/', include('app_top_person.urls')),

    # user keyword analysis
    path('userkeyword/', include('app_user_keyword.urls')),
    
    # app shih chung chen
    path('trump/', include('app_scchen.urls')),
    
    # full text search and associated keyword display
    path('userkeyword_assoc/', include('app_user_keyword_association.urls')),
    
    # user keyword sentiment 
    path('userkeyword_senti/', include('app_user_keyword_sentiment.urls')),
    
    # user keyword sentiment 
    path('userkeyword_report/', include('app_user_keyword_llm_report.urls')),

    # mayor election
    path('', include('app_taipei_mayor.urls')),
    
    path('userkeyword_db/', include('app_user_keyword_db.urls')),
    # admin
    path('admin/', admin.site.urls),
    
    path('poa_intro/', include('app_poa_introduction.urls')),
    
    path('104/', include('app_104.urls', namespace='app_104')), 
    path('104/area_analysis/', include(('app_104.area_analysis.urls', 'area_analysis'), namespace='area_analysis')),
    path('104/tool_analysis/', include(('app_104.tool_analysis.urls', 'tool_analysis'), namespace='tool_analysis')),
    path('104/salary_analysis/', include(('app_104.salary_analysis.urls', 'salary_analysis'), namespace='salary_analysis')),
    path('104/conditional_analysis/', include(('app_104.conditional_analysis.urls', 'conditional_analysis'), namespace='conditional_analysis')),
    path('104/search_keyword/', include(('app_104.search_keyword.urls', 'search_keyword'), namespace='search_keyword')),
    path('104/trait_analysis/', include(('app_104.trait_analysis.urls', 'trait_analysis'), namespace='trait_analysis')),
    path('104/top_keyword/', include(('app_104.top_keyword.urls', 'top_keyword'), namespace='top_keyword')),
    
]


