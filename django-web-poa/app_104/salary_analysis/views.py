from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import os
from django.conf import settings

def home(request):
    # 首頁視圖，會渲染 salary_analysis/home.html 模板
    return render(request, 'salary_analysis/home.html')

def get_average_salary(request):
    
    # 取得各職業類別的平均薪資。若傳入 area 參數，則僅計算該地區資料；否則計算全部資料。
    
    try:
        file_path = os.path.join(settings.BASE_DIR,  'app_104','salary_analysis', 'dataset', 'jobs.csv')
        if not os.path.exists(file_path):
            return JsonResponse({'error': '找不到檔案'}, status=404)

        df = pd.read_csv(file_path, sep='|')
        # 將 final_salary 欄位轉換為數值（無法轉換的設為 NaN）
        df['final_salary'] = pd.to_numeric(df['final_salary'], errors='coerce')
        
        # 取得 area 參數，若存在則過濾該地區（假設以字串開頭判斷）
        area = request.GET.get('area', '')
        if area:
            df = df[df['area'].str.startswith(area)]
        
        # 定義固定的五個職業類別
        job_categories = ["前端工程師", "數據分析師", "AI工程師", "網路管理工程師", "雲端工程師"]
        averages = {}
        for job in job_categories:
            subset = df[df['jobType'] == job]
            if not subset.empty:
                avg_salary = subset['final_salary'].mean()
                averages[job] = round(avg_salary, 2)
            else:
                averages[job] = 0
        return JsonResponse(averages)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_vacancy_counts(request):
    # 取得各地區的職缺數。僅針對指定的地區進行統計。
    try:
        file_path = os.path.join(settings.BASE_DIR,  'app_104','salary_analysis', 'dataset', 'jobs.csv')
        if not os.path.exists(file_path):
            return JsonResponse({'error': '找不到檔案'}, status=404)
        
        df = pd.read_csv(file_path, sep='|')
        
        # 定義需要統計的地區
        areas = ["台北", "基隆", "新北", "桃園", "新竹",
                 "苗栗", "台中", "彰化", "南投", "雲林",
                 "嘉義", "台南", "高雄", "屏東", "宜蘭",
                 "花蓮", "台東"]
        counts = {}
        for area in areas:
            count = df[df['area'].str.startswith(area)].shape[0]
            counts[area] = count
        return JsonResponse(counts)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)