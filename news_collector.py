import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

class NewsCollector:
    def __init__(self):
        # 주요 한국 뉴스 RSS 피드
        self.rss_feeds = {
            'naver_politics': 'https://news.naver.com/main/rss/section.naver?sid1=100',
            'naver_economy': 'https://news.naver.com/main/rss/section.naver?sid1=101',
            'naver_society': 'https://news.naver.com/main/rss/section.naver?sid1=102',
            'naver_world': 'https://news.naver.com/main/rss/section.naver?sid1=104',
        }
        
    def fetch_news_from_rss(self, url, max_items=10):
        """RSS 피드에서 뉴스 수집"""
        try:
            feed = feedparser.parse(url)
            news_items = []
            
            for entry in feed.entries[:max_items]:
                news_item = {
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.get('published', ''),
                    'description': entry.get('description', ''),
                    'timestamp': datetime.now().isoformat()
                }
                news_items.append(news_item)
            
            return news_items
        except Exception as e:
            print(f"RSS 피드 수집 오류: {e}")
            return []
    
    def collect_all_news(self):
        """모든 RSS 피드에서 뉴스 수집"""
        all_news = []
        
        for source, url in self.rss_feeds.items():
            print(f"수집 중: {source}")
            news_items = self.fetch_news_from_rss(url)
            
            for item in news_items:
                item['source'] = source
                all_news.append(item)
        
        print(f"총 {len(all_news)}개의 뉴스 수집 완료")
        return all_news
    
    def get_trending_keywords(self):
        """네이버 실시간 검색어 수집 (예시)"""
        # 실제로는 API 또는 크롤링 필요
        # 여기서는 데모용 더미 데이터
        return [
            "대통령", "국회", "경제성장", "부동산", "주식시장",
            "미국", "중국", "트럼프", "날씨", "지진"
        ]

if __name__ == "__main__":
    collector = NewsCollector()
    news = collector.collect_all_news()
    print(json.dumps(news[:2], indent=2, ensure_ascii=False))
