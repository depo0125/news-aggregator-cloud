import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

class NewsCollector:
    def __init__(self):
        # 다양한 뉴스 RSS 피드 (네이버 외 추가)
        self.rss_feeds = {
            # 네이버 뉴스
            'naver_headline': 'https://news.naver.com/main/rss/section.nhn?sid1=001',
            'naver_politics': 'https://news.naver.com/main/rss/section.nhn?sid1=100',
            'naver_economy': 'https://news.naver.com/main/rss/section.nhn?sid1=101',
            'naver_society': 'https://news.naver.com/main/rss/section.nhn?sid1=102',
            'naver_world': 'https://news.naver.com/main/rss/section.nhn?sid1=104',
            
            # 다음 뉴스 (백업)
            'daum_society': 'https://news.daum.net/rss/society',
            'daum_politics': 'https://news.daum.net/rss/politics',
            'daum_economic': 'https://news.daum.net/rss/economic',
            'daum_foreign': 'https://news.daum.net/rss/foreign',
        }
        
    def fetch_news_from_rss(self, url, max_items=10):
        """RSS 피드에서 뉴스 수집"""
        try:
            # User-Agent 헤더 추가
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # requests로 먼저 가져오기
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # feedparser로 파싱
            feed = feedparser.parse(response.content)
            news_items = []
            
            if not feed.entries:
                print(f"  ⚠️ {url} - 엔트리 없음")
                return []
            
            for entry in feed.entries[:max_items]:
                try:
                    news_item = {
                        'title': entry.get('title', '제목 없음'),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'description': entry.get('description', entry.get('summary', '')),
                        'timestamp': datetime.now().isoformat()
                    }
                    news_items.append(news_item)
                except Exception as e:
                    print(f"  ⚠️ 개별 뉴스 파싱 오류: {e}")
                    continue
            
            print(f"  ✓ {len(news_items)}개 수집 성공")
            return news_items
            
        except requests.exceptions.RequestException as e:
            print(f"  ✗ HTTP 요청 실패: {e}")
            return []
        except Exception as e:
            print(f"  ✗ RSS 피드 수집 오류: {e}")
            return []
    
    def collect_all_news(self):
        """모든 RSS 피드에서 뉴스 수집"""
        all_news = []
        successful_sources = 0
        
        print("=" * 50)
        print("뉴스 수집 시작...")
        print("=" * 50)
        
        for source, url in self.rss_feeds.items():
            print(f"\n📡 {source} 수집 중...")
            print(f"   URL: {url}")
            
            news_items = self.fetch_news_from_rss(url, max_items=5)
            
            if news_items:
                successful_sources += 1
                for item in news_items:
                    item['source'] = source
                    all_news.append(item)
        
        print("\n" + "=" * 50)
        print(f"✅ 수집 완료: {len(all_news)}개 뉴스")
        print(f"📊 성공한 소스: {successful_sources}/{len(self.rss_feeds)}")
        print("=" * 50)
        
        return all_news
    
    def get_trending_keywords(self):
        """실시간 검색어 (더미 데이터)"""
        return [
            "대통령", "국회", "경제성장", "부동산", "주식시장",
            "미국", "중국", "트럼프", "날씨", "지진"
        ]

if __name__ == "__main__":
    collector = NewsCollector()
    news = collector.collect_all_news()
    print(f"\n총 {len(news)}개의 뉴스 수집됨")
    if news:
        print("\n첫 번째 뉴스:")
        print(json.dumps(news[0], indent=2, ensure_ascii=False))
