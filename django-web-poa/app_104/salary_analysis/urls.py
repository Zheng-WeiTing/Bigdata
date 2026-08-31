from django.urls import path
from . import views

app_name = 'salary_analysis'

urlpatterns = [
    # 首頁：載入 home view
    path('', views.home, name='home'),
    # API：依據是否傳入 area 參數，取得各職業類別的平均薪資
    path('api/salary/average/', views.get_average_salary, name='get_average_salary'),
    # API：取得各地區職缺數
    path('api/salary/vacancies/', views.get_vacancy_counts, name='get_vacancies'),
]