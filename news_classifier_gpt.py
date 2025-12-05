import os
from openai import OpenAI
import json

class NewsClassifierGPT:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
            print("Warning: OPENAI_API_KEY not set. Using fallback classification.")
    
    def classify_and_summarize_with_ai(self, news_items):
        """ChatGPT를 사용한 뉴스 분류 및 요약"""
        if not self.client:
            return self.classify_fallback(news_items)
        
        try:
            # 뉴스 제목들을 하나의 텍스트로 구성
            news_text = "\n".join([
                f"{i+1}. {item['title']}" 
                for i, item in enumerate(news_items)
            ])
            
            prompt = f"""다음 뉴스 제목들을 분석하여 각각을 카테고리로 분류하고 간단히 요약해주세요.

카테고리:
- 정치/정책: 정부, 국회, 정당, 정책 관련
- 사건/사고: 범죄, 재난, 사건사고
- 경제/주식: 경제지표, 기업, 주식시장, 금융
- 부동산: 아파트, 주택, 부동산 정책
- 글로벌: 국제 뉴스 (미국 제외)
- 미국: 미국 관련 뉴스
- 기타: 위 카테고리에 속하지 않는 뉴스

뉴스 목록:
{news_text}

각 뉴스에 대해 다음 JSON 형식으로만 응답해주세요 (다른 설명 없이):
{{
  "results": [
    {{
      "index": 1,
      "category": "카테고리명",
      "summary": "한 줄 요약"
    }}
  ]
}}"""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # 가성비 좋은 모델
                messages=[
                    {"role": "system", "content": "당신은 뉴스 분류 및 요약 전문가입니다. JSON 형식으로만 응답하세요."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            response_text = response.choices[0].message.content
            
            # JSON 파싱
            try:
                # ```json ... ``` 형태의 마크다운 제거
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0]
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0]
                
                result = json.loads(response_text.strip())
                
                # 결과를 원본 뉴스 아이템에 병합
                for item in result.get('results', []):
                    idx = item['index'] - 1
                    if 0 <= idx < len(news_items):
                        news_items[idx]['category'] = item['category']
                        news_items[idx]['summary'] = item['summary']
                
                return news_items
            
            except json.JSONDecodeError as e:
                print(f"JSON 파싱 오류: {e}")
                print(f"응답: {response_text}")
                return self.classify_fallback(news_items)
        
        except Exception as e:
            print(f"AI 분류 오류: {e}")
            return self.classify_fallback(news_items)
    
    def classify_fallback(self, news_items):
        """키워드 기반 간단한 분류 (AI 사용 불가시)"""
        category_keywords = {
            '정치/정책': ['대통령', '국회', '정부', '장관', '의원', '정당', '여당', '야당', '법안', '정책'],
            '사건/사고': ['사고', '화재', '사망', '부상', '경찰', '검찰', '범죄', '체포', '구속'],
            '경제/주식': ['경제', '주가', '코스피', '증시', '기업', '수출', 'GDP', '금리', '은행', '삼성', 'SK', 'LG'],
            '부동산': ['아파트', '집값', '부동산', '주택', '분양', '재건축'],
            '글로벌': ['중국', '일본', '유럽', 'EU', '러시아', '우크라이나', '중동'],
            '미국': ['미국', '트럼프', '바이든', '백악관', '워싱턴', '연준'],
        }
        
        for item in news_items:
            title = item['title'].lower()
            item['category'] = '기타'
            item['summary'] = item.get('description', item['title'])[:100]
            
            for category, keywords in category_keywords.items():
                if any(keyword in title for keyword in keywords):
                    item['category'] = category
                    break
        
        return news_items
    
    def organize_by_category(self, news_items):
        """카테고리별로 뉴스 정리"""
        categorized = {}
        
        for item in news_items:
            category = item.get('category', '기타')
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(item)
        
        # 각 카테고리 내에서 시간순 정렬 (최신순)
        for category in categorized:
            categorized[category].sort(
                key=lambda x: x.get('timestamp', ''), 
                reverse=True
            )
        
        return categorized

if __name__ == "__main__":
    # 테스트
    classifier = NewsClassifierGPT()
    
    sample_news = [
        {'title': '대통령, 경제정책 발표', 'description': '새로운 경제정책 발표'},
        {'title': '코스피 상승세 지속', 'description': '주식시장 호조'},
        {'title': '서울 아파트 가격 상승', 'description': '부동산 시장 과열'},
    ]
    
    result = classifier.classify_fallback(sample_news)
    print(json.dumps(result, indent=2, ensure_ascii=False))
