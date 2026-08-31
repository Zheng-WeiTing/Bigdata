from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import pandas as pd
import os
import ast


# 讀取個人特質資料
def load_data():
    csv_path = os.path.join(
        settings.BASE_DIR,
        'app_104',
        'trait_analysis',
        'dataset',
        '104_personality_traits.csv'
    )

    return pd.read_csv(csv_path)


# 首頁
def home(request):
    df = load_data()

    # 取得所有職業類別並去除重複
    job_types = df['jobType'].drop_duplicates().tolist()

    return render(request, 'trait_analysis/home.html', {
        'job_types': job_types
    })


# 取得個人特質資料
def get_traits_data(request):
    try:
        job_type = request.GET.get('jobType', '全部')
        df = load_data()

        # 取得所有職業的雷達圖資料（排除「全部」）
        filtered_df = df[df['jobType'] != '全部']

        alltraits = {}

        for _, row in filtered_df.iterrows():
            job = row['jobType']
            alltraits[job] = ast.literal_eval(row['alltraits'])

        # 取得文字雲資料
        selected_df = df[df['jobType'] == job_type]

        # 找不到職業
        if selected_df.empty:
            return JsonResponse({
                'error': '找不到指定的職業類別'
            }, status=404)

        row = selected_df.iloc[0]
        traits = ast.literal_eval(row['traits'])

        return JsonResponse({
            'traits': traits,
            'alltraits': alltraits
        })

    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)