from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
import requests
from app_user_keyword.views import filter_dataFrame
import app_user_keyword.views as userkeyword_views

# (1) Load news data
def load_df_data_v1():
    global df
    df = pd.read_csv('app_user_keyword_sentiment/dataset/ltn_news_preprocessed.csv', sep='|')

def home(request):
    return render(request, 'app_user_keyword_sentiment/home.html')

@csrf_exempt
def api_get_userkey_sentiment_from_remote_api_through_backend(request):
    try:
        userkey = request.POST['userkey']
        cate = request.POST['cate']
        cond = request.POST['cond']
        weeks = int(request.POST['weeks'])

        url_api_get_sentiment = "http://163.18.23.20:8000/userkeyword_senti/api_get_userkey_sentiment/"
        sentiment_data = {
            'userkey': userkey,
            'cate': cate,
            'cond': cond,
            'weeks': weeks
        }
        
        sentiment_response = requests.post(url_api_get_sentiment, data=sentiment_data, timeout=5)
        
        if sentiment_response.status_code == 200:
            print("由後端呼叫他處API，取得情感分析數據成功!")
            return JsonResponse(sentiment_response.json())
        else:
            print(f"回傳有錯誤，進行本地處理資料")
            return JsonResponse({'error': 'Failed to get sentiment analysis.'})
    except Exception as e:
        print(f"呼叫異常失敗，進行本地處理資料: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def api_get_userkey_sentiment(request):
    try:
        userkey = request.POST['userkey']
        cate = request.POST['cate']
        cond = request.POST['cond']
        weeks = int(request.POST['weeks'])

        query_keywords = userkey.split()
        df_query = filter_dataFrame(query_keywords, cond, cate, weeks).copy()  # 創 建一個副本
        


        # 將sentiment欄位中的 "暫無" 轉換為0
        df_query.loc[:, 'sentiment'] = pd.to_numeric(df_query['sentiment'], errors='coerce').fillna(1)

        sentiCount, sentiPercnt = get_article_sentiment(df_query)
        freq_type = 'D' if weeks <= 4 else 'W'
        
        response = {
            'sentiCount': sentiCount,
            'sentiPercnt': sentiPercnt,
            'data_pos': get_daily_basis_sentiment_count(df_query, 'pos', freq_type),
            'data_neg': get_daily_basis_sentiment_count(df_query, 'neg', freq_type),
            'data_neutral': get_daily_basis_sentiment_count(df_query, 'neutral', freq_type)
        }
        
        print("Response data:", response)
        return JsonResponse(response)
        
    except Exception as e:
        print(f"Error in api_get_userkey_sentiment: {str(e)}")
        return JsonResponse({'error': f'處理資料時發生錯誤：{str(e)}'}, status=500)
    


def get_article_sentiment(df_query):
    sentiCount = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    sentiPercnt = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    numberOfArticle = len(df_query)
    
    for idx, senti in enumerate(df_query.sentiment):
        
        # 判斷情感極性
        if float(senti) >= 0.6:
            sentiCount['Positive'] += 1
            print("正面")
        elif float(senti) <= 0.4:
            sentiCount['Negative'] += 1
            print("負面")
        else:
            sentiCount['Neutral'] += 1
            print("中立")
    
    # 計算百分比
    if numberOfArticle > 0:
        for polar in sentiCount:
            sentiPercnt[polar] = int(sentiCount[polar]/numberOfArticle*100)
    
    
    return sentiCount, sentiPercnt

def get_daily_basis_sentiment_count(df_query, sentiment_type='pos', freq_type='D'):
    def get_sentiment_value(senti):
        try:
            value = float(senti)
            if sentiment_type == 'pos':
                return 1 if value >= 0.6 else 0
            elif sentiment_type == 'neg':
                return 1 if value <= 0.4 else 0
            elif sentiment_type == 'neutral':
                return 1 if 0.4 < value < 0.6 else 0
            return 0
        except (ValueError, TypeError):
            return 0  # 處理 "暫無" 的情況
    
    try:
        # 建立新的 DataFrame
        freq_df = pd.DataFrame({
            'date_index': pd.to_datetime(df_query['date']),
            'frequency': [get_sentiment_value(senti) for senti in df_query['sentiment']],
            'sentiment': df_query['sentiment']  # 加入原始情感分數以便除錯
        })
        
        
        # 依照時間分組
        freq_df_group = freq_df.groupby(pd.Grouper(key='date_index', freq=freq_type))['frequency'].sum().reset_index()
        
        # 產生圖表資料
        xy_line_data = [
            {'x': date.strftime('%Y-%m-%d'), 'y': int(freq)}
            for date, freq in zip(freq_df_group['date_index'], freq_df_group['frequency'])
            if pd.notna(freq)
        ]
        
        # 如果沒有資料，加入預設值
        if not xy_line_data:
            today = pd.Timestamp.now()
            xy_line_data.append({
                'x': today.strftime('%Y-%m-%d'),
                'y': 0
            })
        
        return xy_line_data
        
    except Exception as e:
        print(f"Error in get_daily_basis_sentiment_count: {str(e)}")
        return []


# 初始化資料
load_df_data_v1()
print("app_userkey_sentiment was loaded!")
