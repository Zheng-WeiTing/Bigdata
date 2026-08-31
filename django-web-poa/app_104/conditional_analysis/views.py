import pandas as pd
import os
import re
from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    return render(request, 'conditional_analysis/home.html')

def conditional_analysis(request):
    job_type = request.GET.get('jobType', '全部')
    condition = request.GET.get('condition', 'workExp')
    y_axis = request.GET.get('yAxis', 'count')  # 添加 y_axis 參數

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(BASE_DIR, 'conditional_analysis', 'dataset', 'jobs.csv')    
    df = pd.read_csv(csv_path, delimiter='|')

    if job_type != "全部":
        df = df[df['jobType'] == job_type]

    if condition == 'workExp':
        def parse_exp(val):
            val = str(val).strip()
            if '不拘' in val:
                return '不拘'
            match = re.search(r'(\d+)', val)
            if match:
                year = int(match.group(1))
                return f'{year}年以上' if year < 5 else '5年以上'
            return '不拘'

        df['parsed_exp'] = df['workExp'].apply(parse_exp)
        exp_order = ['不拘', '1年以上', '2年以上', '3年以上', '4年以上', '5年以上']
        
        if y_axis == 'salary':
            # 計算每個經歷層級的平均薪資
            salary_means = df.groupby('parsed_exp')['final_salary'].mean()
            counts = salary_means.reindex(exp_order, fill_value=0)
            # 四捨五入到千位
            counts = counts.round(-3)
        else:
            counts = df['parsed_exp'].value_counts().reindex(exp_order, fill_value=0)
        
        labels = counts.index.tolist()

    elif condition == 'edu':
        # 直接取 edu 欄位的前兩個字
        df['parsed_edu'] = df['edu'].str[:2]
        # 處理「不拘」的情況
        df.loc[df['edu'].str.contains('不拘', na=False), 'parsed_edu'] = '不拘'
        
        edu_order = ['不拘', '高中', '專科', '大學', '碩士', '博士']
        
        if y_axis == 'salary':
            # 計算每個學歷層級的平均薪資
            salary_means = df.groupby('parsed_edu')['final_salary'].mean()
            counts = salary_means.reindex(edu_order, fill_value=0)
            # 四捨五入到千位
            counts = counts.round(-3)
        else:
            # 計算各學歷的職缺數量
            counts = df['parsed_edu'].value_counts().reindex(edu_order, fill_value=0)
        
        labels = counts.index.tolist()

    else:
        return JsonResponse({'error': 'Invalid condition'}, status=400)

    return JsonResponse({
        'labels': labels,
        'counts': counts.tolist()
    })