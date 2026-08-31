from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import re
import os
from django.conf import settings



def home(request):
    return render(request, 'search_keyword/home.html')

@csrf_exempt
def api_get_top_userkey(request):
    userkey = request.GET.get('userkey')
    cate = request.GET.get('cate')
    cond = request.GET.get('cond')
    weeks = int(request.GET.get('weeks'))
    key = userkey.lower().split()
    
    global  df_query 

    df_query = filter_dataFrame(key, cond, cate,weeks) # 篩選成符合條件的資料
    key_freq_cat, key_occurrence_cat = count_keyword(df_query, key)    # 統計職缺數 & 關鍵字提及數
    key_time_freq = get_keyword_time_based_freq(df_query) # 統計每天有幾筆符合條件的職缺

    response = {
    'key_occurrence_cat': key_occurrence_cat,  # 左側比較圖資料
    'key_freq_cat': key_freq_cat,  # 左側比較圖資料
    'key_time_freq': key_time_freq, } # 右側時間趨勢資料

    return JsonResponse(response)



def filter_dataFrame(user_keywords, cond, cate, weeks):
    file_path = os.path.join(settings.BASE_DIR,  'app_104','search_keyword', 'dataset', '104_preprocessed.csv')
    df = pd.read_csv(file_path, sep='|')
    end_date = df.date.max()
    start_date = (datetime.strptime(end_date, '%Y-%m-%d').date() - timedelta(weeks=weeks)).strftime('%Y-%m-%d')
    period_condition = (df.date >= start_date) & (df.date <= end_date) 

    # 根據使用者選擇的職缺類別篩選資料(在時間範圍內)
    if (cate == "全部"):
        condition = period_condition  
    else:
        condition = period_condition & (df.jobType == cate)

    # 根據使用者輸入的關鍵字和邏輯運算符篩選資料(在時間範圍內)
    if (cond == 'and'):
        condition = condition & df.apply(lambda row: all((
            (qk in str(row.jobDetail).lower()) or 
            (qk in str(row.welfare).lower())
        ) for qk in user_keywords), axis=1)
    elif (cond == 'or'):
        condition = condition & df.apply(lambda row: any((
            (qk in str(row.jobDetail).lower()) or 
            (qk in str(row.welfare).lower())
        ) for qk in user_keywords), axis=1)
    
    df_query = df[condition]
    return df_query


news_categories = ['前端工程師', '數據分析師', 'AI工程師', '網路管理工程師', '雲端工程師', '全部']

def count_keyword(df_query, query_keywords):
    cate_occurrence = {} # 職缺數
    cate_freq = {} # 提及數
    
    # 字典初始化
    for cate in news_categories:
        cate_occurrence[cate] = 0
        cate_freq[cate] = 0

    for idx, row in df_query.iterrows():
        cate_occurrence[row.jobType] += 1
        cate_occurrence['全部'] += 1
        
        # 計算關鍵字在 jobDetail 和 welfare 中的出現頻率
        freq_detail = sum([len(re.findall(keyword, str(row.jobDetail).lower(), re.I)) for keyword in query_keywords])
        freq_welfare = sum([len(re.findall(keyword, str(row.welfare).lower(), re.I)) for keyword in query_keywords])
        
        # 合併兩個欄位的頻率
        total_freq = freq_detail + freq_welfare
        
        cate_freq[row.jobType] += total_freq
        cate_freq['全部'] += total_freq

    return cate_freq, cate_occurrence


def get_keyword_time_based_freq(df_query):
    date_samples = df_query.date
    query_freq = pd.DataFrame({'date_index': pd.to_datetime(date_samples), 'freq': [1 for _ in range(len(df_query))]})
    data = query_freq.groupby(pd.Grouper(key='date_index', freq='D')).sum()['freq']
    time_data = []
    for i, idx in enumerate(data.index):
        row = {'x': idx.strftime('%Y-%m-%d'), 'y': int(data.iloc[i])}
        time_data.append(row)
    return time_data


