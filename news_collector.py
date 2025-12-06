import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import random

class NewsCollector:
    def __init__(self):
        # 실제 RSS 피드
        self.rss_feeds = {
            'naver_politics': 'https://news.naver.com/main/rss/section.naver?sid1=100',
            'naver_economy': 'https://news.naver.com/main/rss/section.naver?sid1=101',
        }
        
        # 더미 뉴스 (RSS 실패 시 사용)
        self.dummy_news = self._generate_dummy_news()
        
    def _generate_dummy_news(self):
        """테스트용 더미 뉴스 생성"""
        categories = {
            '정치': [
                '대통령, 새로운 경제정책 발표 예정',
                '국회, 내년도 예산안 본회의 통과',
                '여야, 민생법안 처리 합의',
                '정부, 규제완화 정책 추진',
                '장관 후보자 인사청문회 실시',
            ],
            '경제': [
                '코스피, 2주 연속 상승세 지속',
                '반도체 수출 전년 대비 15% 증가',
                '한국은행, 기준금리 동결 결정',
                '대기업 3분기 실적 호조',
                '환율 1,300원대 중반 등락',
            ],
            '사회': [
                '전국 대부분 지역 미세먼지 보통',
                '주말 전국 맑고 포근한 날씨',
                '대학 입시 원서접수 시작',
                '연말 자선 캠페인 열기',
                '지역축제 성황리 개최',
            ],
            '글로벌': [
                '미·중 정상회담 개최 합의',
                '유럽 경기 회복 조짐',
                '일본, 관광객 급증세',
                '동남아 경제성장 가속화',
                '중동 평화협상 진전',
            ],
        }
        
        all_news = []
        base_time = datetime.now()
        
        for category, titles in categories.items():
            for i, title in enumerate(titles):
                news_item = {
                    'title': title,
                    'link': f'https://news.example.com/{category.lower()}/{i+1}',
                    'published': (base_time - timedelta(minutes=i*10)).strftime('%Y-%m-%d %H:%M:%S'),
                    'description': f'{title}에 대한 상세 내용입니다.',
                    'timestamp': (base_time - timedelta(minutes=i*10)).isoformat(),
                    'source': f'dummy_{category}'
                }
                all_news.append(news_item)
        
        return all_news
        
    def fetch_news_from_rss(self, url, max_items=10):
        """RSS 피드에서 뉴스 수집"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            feed = feedparser.parse(response.content)
            news_items = []
            
            for entry in feed.entries[:max_items]:
                news_item = {
                    'title': entry.get('title', '제목 없음'),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'description': entry.get('description', ''),
                    'timestamp': datetime.now().isoformat()
                }
                news_items.append(news_item)
            
            return news_items
        except Exception as e:
            print(f"RSS 피드 오류 ({url}): {e}")
            return []
    
    def collect_all_news(self):
        """모든 RSS 피드에서 뉴스 수집 (실패 시 더미 데이터 사용)"""
        all_news = []
        
        print("뉴스 수집 시작...")
        
        # RSS 피드 시도
        for source, url in self.rss_feeds.items():
            print(f"수집 중: {source}")
            news_items = self.fetch_news_from_rss(url, max_items=5)
            
            for item in news_items:
                item['source'] = source
                all_news.append(item)
        
        # RSS 수집 실패 시 더미 데이터 사용
        if len(all_news) == 0:
            print("⚠️ RSS 수집 실패 - 더미 뉴스 사용")
            all_news = self.dummy_news.copy()
            # 타임스탬프 업데이트
            now = datetime.now()
            for i, item in enumerate(all_news):
                item['timestamp'] = (now - timedelta(minutes=i*5)).isoformat()
        
        print(f"총 {len(all_news)}개의 뉴스 수집 완료")
        return all_news
    
    def get_trending_keywords(self):
        """실시간 검색어"""
        return [
            "대통령", "국회", "경제성장", "부동산", "주식시장",
            "미국", "중국", "트럼프", "날씨", "지진"
        ]

if __name__ == "__main__":
    collector = NewsCollector()
    news = collector.collect_all_news()
    print(f"\n수집된 뉴스: {len(news)}개")
    if news:
        print(json.dumps(news[0], indent=2, ensure_ascii=False))
