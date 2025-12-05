from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from news_collector import NewsCollector
from news_classifier_gpt import NewsClassifierGPT
import threading
import time
import json
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')
CORS(app)  # 프론트엔드에서 API 호출 가능하도록 CORS 설정

# 전역 변수로 최신 뉴스 저장
latest_news = {
    'data': {},
    'last_updated': None,
    'total_count': 0
}

# 뉴스 수집기 및 분류기 초기화
collector = NewsCollector()
classifier = NewsClassifierGPT()

def update_news():
    """뉴스 수집 및 분류 업데이트"""
    global latest_news
    
    try:
        print(f"[{datetime.now()}] 뉴스 수집 시작...")
        
        # 1. 뉴스 수집
        news_items = collector.collect_all_news()
        
        if not news_items:
            print("수집된 뉴스가 없습니다.")
            return
        
        # 2. AI 분류 및 요약 (처음 30개만)
        news_to_classify = news_items[:30]
        classified_news = classifier.classify_and_summarize_with_ai(news_to_classify)
        
        # 나머지는 간단 분류
        remaining_news = news_items[30:]
        if remaining_news:
            remaining_news = classifier.classify_fallback(remaining_news)
        
        all_classified = classified_news + remaining_news
        
        # 3. 카테고리별 정리
        categorized = classifier.organize_by_category(all_classified)
        
        # 4. 전역 변수 업데이트
        latest_news = {
            'data': categorized,
            'last_updated': datetime.now().isoformat(),
            'total_count': len(all_classified)
        }
        
        print(f"[{datetime.now()}] 뉴스 업데이트 완료: {len(all_classified)}개")
        print(f"카테고리: {list(categorized.keys())}")
        
    except Exception as e:
        print(f"뉴스 업데이트 오류: {e}")

def scheduled_update():
    """주기적으로 뉴스 업데이트 (30분마다)"""
    while True:
        update_news()
        time.sleep(1800)  # 30분 = 1800초

# 프론트엔드 서빙
@app.route('/')
def serve_frontend():
    """프론트엔드 HTML 제공"""
    return send_from_directory('static', 'index.html')

@app.route('/api/status')
def api_status():
    """API 상태 확인"""
    return jsonify({
        'status': 'running',
        'message': '뉴스 수집 API 서버',
        'last_updated': latest_news.get('last_updated'),
        'total_news': latest_news.get('total_count', 0),
        'endpoints': {
            '/': '프론트엔드',
            '/api/news': '전체 뉴스 조회',
            '/api/news/<category>': '카테고리별 뉴스 조회',
            '/api/refresh': '수동 뉴스 갱신'
        }
    })

@app.route('/api/news', methods=['GET'])
def get_all_news():
    """전체 뉴스 조회"""
    return jsonify(latest_news)

@app.route('/api/news/<category>', methods=['GET'])
def get_news_by_category(category):
    """특정 카테고리 뉴스 조회"""
    category_data = latest_news['data'].get(category, [])
    
    return jsonify({
        'category': category,
        'count': len(category_data),
        'news': category_data,
        'last_updated': latest_news['last_updated']
    })

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """사용 가능한 카테고리 목록"""
    categories = list(latest_news['data'].keys())
    category_counts = {
        cat: len(latest_news['data'][cat]) 
        for cat in categories
    }
    
    return jsonify({
        'categories': categories,
        'counts': category_counts
    })

@app.route('/api/refresh', methods=['POST'])
def refresh_news():
    """수동으로 뉴스 갱신"""
    try:
        update_news()
        return jsonify({
            'status': 'success',
            'message': '뉴스가 갱신되었습니다.',
            'total_count': latest_news['total_count']
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    # 서버 시작 시 한 번 뉴스 수집
    print("초기 뉴스 수집 중...")
    update_news()
    
    # 백그라운드 스레드로 주기적 업데이트 시작
    update_thread = threading.Thread(target=scheduled_update, daemon=True)
    update_thread.start()
    
    # Flask 서버 실행
    port = int(os.environ.get('PORT', 5000))
    print(f"Flask 서버 시작... (포트: {port})")
    app.run(host='0.0.0.0', port=port, debug=False)
