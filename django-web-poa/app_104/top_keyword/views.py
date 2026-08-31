import json
import pandas as pd
from django.shortcuts import render
import os
from django.conf import settings
from django.http import JsonResponse


def home(request):
    return render(request, 'top_keyword/home.html')

def get_keywords(request):
    csv_path = os.path.join(settings.BASE_DIR,  'app_104','top_keyword', 'dataset', '104_general_keywords.csv')
    df = pd.read_csv(csv_path)
    job_type = request.GET.get('job_type', '前端工程師')
    top_n = int(request.GET.get('top_n', 10))

    try:
        if job_type == '全部':
            job_types = ['前端工程師', '數據分析師', 'AI工程師', '網路管理工程師', '雲端工程師']
            color_palette = [
                "rgba(114, 47, 55, 0.7)",    # 前端工程師 - 深紅
                "rgba(235,160,80, 0.7)",   # 數據分析師 - 橘色
                "rgba(62, 115, 93, 0.7)",   # AI工程師 - 青綠
                "rgba(64, 73, 118, 0.7)",  # 網路管理工程師 - 淺藍
                "rgba(150,130,160, 0.7)",  # 雲端工程師 - 淡紫
            ]

            keyword_set = set() # 去除重複值
            job_keywords = {} # 存每個職業自己的關鍵字

            # 先整理每個職業的關鍵字字典（只取 top_n）
            for job in job_types:
                row = df[df['jobType'] == job].iloc[0]
                kw_list = eval(row['keywords'])[:top_n]  # 取前 top_n 個關鍵字
                job_keywords[job] = dict(kw_list)
                keyword_set.update([kw[0] for kw in kw_list])

            # 計算所有關鍵字的總出現次數
            keyword_total_count = {}
            for job in job_types:
                for kw, cnt in job_keywords[job].items():
                    keyword_total_count[kw] = keyword_total_count.get(kw, 0) + cnt

            # 排序取前 top_n 熱門關鍵字（依照總次數）
            sorted_keywords = sorted(keyword_total_count.items(), key=lambda x: x[1], reverse=True)
            top_keywords = [kw[0] for kw in sorted_keywords[:top_n]]

            # 每個職業對應的關鍵字數據（補 0），因爲 Chart.js 需要每個職業的數據長度一致
            datasets = []
            for idx, job in enumerate(job_types):
                job_data = [job_keywords[job].get(kw, 0) for kw in top_keywords]
                datasets.append({
                    "label": job,
                    "data": job_data,
                    "backgroundColor": color_palette[idx] # 有 idx 的原因是因為要加入顏色
                })

            # 準備加總表格資料
            totals = [{"word": kw, "count": keyword_total_count[kw]} for kw in top_keywords]

            return JsonResponse({
                "job_type": "全部",
                "labels": top_keywords,
                "datasets": datasets,
                "totals": totals
            })

        else:
            # 單一職業：直接回傳前 top_n 個關鍵字
            row = df[df['jobType'] == job_type].iloc[0]
            kw_list = eval(row['keywords'])[:top_n]
            return JsonResponse({
                "job_type": job_type,
                "keywords": [{"word": k[0], "count": k[1]} for k in kw_list]
            })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)