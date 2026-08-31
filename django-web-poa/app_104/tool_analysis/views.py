from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from collections import Counter
import os
from django.conf import settings

def home(request):
    return render(request, 'tool_analysis/home.html')

def get_wordcloud_data(request, job_type='全部'):
    csv_path = os.path.join(settings.BASE_DIR,  'app_104','tool_analysis', 'dataset', 'jobs.csv')
    df = pd.read_csv(csv_path, delimiter='|')
    
    if job_type != "全部":
        df = df[df['jobType'] == job_type]
    
    tools = []
    for tools_str in df['tool'].dropna():
        tools.extend([t.strip() for t in tools_str.split(',')])

    tool_counts = Counter(tools)
    # 回傳所有資料，讓前端決定要顯示多少筆
    data = [{"text": tool, "value": count} for tool, count in tool_counts.most_common()]
    
    return JsonResponse(data, safe=False)

def get_bubble_data(request):
    csv_path = os.path.join(settings.BASE_DIR,  'app_104','tool_analysis', 'dataset', 'jobs.csv')
    df = pd.read_csv(csv_path, delimiter='|')
    
    # 指定固定的顏色對應
    job_color_mapping = {
        "前端工程師": "#800000",    # 酒紅色
        "數據分析師": "#DAA520",    # 深藍色
        "AI工程師": "#275F3E",      # 灰色
        "網路管理工程師": "#00008B", # 綠色 (使用 rgb(39,95,62) 的色系)
        "雲端工程師": "#505050"      # 深一點的黃棕色
    }
    
    bubble_data = []
    for job_type, base_color in job_color_mapping.items():
        job_df = df[df['jobType'] == job_type]
        tools = []
        for tool_str in job_df['tool'].dropna():
            tools.extend([t.strip() for t in tool_str.split(',')])
        
        tool_counts = Counter(tools)
        for tool, count in tool_counts.items():
            bubble_data.append({
                "name": tool,
                "group": job_type,
                "value": count,
                "color": base_color
            })
        
    return JsonResponse(bubble_data, safe=False)