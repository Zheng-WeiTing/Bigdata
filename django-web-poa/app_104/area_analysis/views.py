import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
import os
from django.conf import settings

def home(request):
    return render(request, 'area_analysis/home.html')

def get_jobs(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'app_104', 'area_analysis', 'dataset', 'jobs.csv')
        if not os.path.exists(file_path):
            return JsonResponse({'error': '找不到檔案'}, status=404)

        df = pd.read_csv(file_path, sep='|')
        df = df.where(pd.notnull(df), None)

        job_type = request.GET.get('job_type', '全部') #取得職業類別
        area = request.GET.get('area', None) #取得地區

        if job_type != '全部':
            df = df[df['jobType'] == job_type] #篩選資料
        if area:
            df = df[df['area'].str.startswith(area)] #如果有地區就篩選資料

        area_counts_raw = df['area'].value_counts().to_dict() #統計各地區職缺數量，並轉成字典
        # 例如：{ '台北市中正區': 10, '台北市大安區': 15, '新北市板橋區': 20, ...}


        # 轉換 key：把「台北市中正區」變成「台北」
        area_counts = {}
        for full_area, count in area_counts_raw.items():
            short_area = full_area[:2]
            area_counts[short_area] = area_counts.get(short_area, 0) + count # 累加各區數量

        # 回傳 JSON 格式的資料給前端
        return JsonResponse({
            'jobs': df.to_dict('records'), # 把篩選後的 df 轉成 list of dict
            'area_counts': area_counts     # 回傳各地區職缺數量
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)