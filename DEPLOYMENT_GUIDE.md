# 🚀 클라우드 배포 가이드 (ChatGPT + Render)

## 📋 준비물

1. ✅ GitHub 계정 (무료) - https://github.com
2. ✅ Render 계정 (무료) - https://render.com
3. ✅ OpenAI API Key (유료) - https://platform.openai.com

---

## 💰 비용 안내

### 무료
- GitHub: 완전 무료
- Render: 매월 750시간 무료 (24/7 운영 가능)

### 유료
- **OpenAI API**: 월 $5-20 예상
  - GPT-4o-mini 사용 시: 매우 저렴 ($0.15/1M 입력 토큰)
  - 하루 100개 뉴스 분류 시: 월 $3-5 정도
  - API Key만 있으면 사용한 만큼만 지불

---

## 🔑 1단계: OpenAI API Key 발급

### 1. OpenAI 가입
1. https://platform.openai.com 접속
2. 계정 생성 (Google/Microsoft 계정으로 간편 가입)
3. 전화번호 인증

### 2. 결제 수단 등록
1. Settings → Billing 메뉴
2. "Add payment method" 클릭
3. 신용카드/체크카드 등록
4. 최소 $5 충전 (사용한 만큼만 차감)

### 3. API Key 생성
1. API Keys 메뉴 선택
2. "Create new secret key" 클릭
3. 이름 입력 (예: "news-app")
4. **Key 복사 후 안전하게 보관!** (다시 볼 수 없음)
   - 형식: `sk-proj-...` 로 시작하는 긴 문자열

---

## 📦 2단계: GitHub에 코드 업로드

### 방법 1: GitHub Desktop 사용 (초보자 추천)

1. **GitHub Desktop 설치**
   - https://desktop.github.com 에서 다운로드
   - 설치 후 GitHub 계정 로그인

2. **저장소 생성**
   - File → New Repository
   - Name: `news-aggregator`
   - Local Path: 다운로드 받은 프로젝트 폴더 선택
   - "Create Repository" 클릭

3. **코드 업로드**
   - "Publish repository" 클릭
   - Public 체크 (무료로 사용하려면)
   - "Publish Repository" 클릭

### 방법 2: Git 명령어 사용

```bash
# 프로젝트 폴더로 이동
cd news-aggregator-cloud

# Git 초기화
git init

# GitHub에 저장소 생성 후 연결
git remote add origin https://github.com/본인계정/news-aggregator.git

# 파일 추가
git add .

# 커밋
git commit -m "Initial commit"

# 업로드
git push -u origin main
```

---

## 🌐 3단계: Render에 배포

### 1. Render 가입
1. https://render.com 접속
2. "Get Started for Free" 클릭
3. GitHub 계정으로 가입

### 2. GitHub 연결
1. Render 대시보드에서 "Connect GitHub" 클릭
2. 권한 승인
3. `news-aggregator` 저장소 선택

### 3. 웹 서비스 생성
1. "New +" → "Web Service" 클릭
2. GitHub 저장소 선택: `news-aggregator`
3. 설정 입력:

```
Name: news-aggregator (또는 원하는 이름)
Region: Singapore (가장 가까운 지역)
Branch: main
Root Directory: (비워둠)
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
Instance Type: Free
```

### 4. 환경 변수 설정 (중요!)
스크롤 내려서 "Environment Variables" 섹션:

1. "Add Environment Variable" 클릭
2. Key: `OPENAI_API_KEY`
3. Value: (위에서 복사한 OpenAI API Key 붙여넣기)
4. "Add" 클릭

### 5. 배포 시작
- "Create Web Service" 클릭
- 5-10분 정도 기다리면 배포 완료!

### 6. 접속 확인
- 배포 완료 후 URL 생성됨 (예: `https://news-aggregator-xxxx.onrender.com`)
- 해당 URL로 접속하면 웹 앱 실행!

---

## 📱 4단계: 모바일에서 사용하기

### 홈 화면에 추가 (PWA처럼 사용)

**iPhone (Safari):**
1. Render에서 제공한 URL 접속
2. 공유 버튼 탭
3. "홈 화면에 추가" 선택
4. 이름 입력 후 추가

**Android (Chrome):**
1. URL 접속
2. 메뉴(⋮) → "홈 화면에 추가"
3. 이름 입력 후 추가

이제 앱처럼 사용 가능! 📱

---

## 🔧 문제 해결

### 배포가 실패할 때
1. Render 대시보드에서 "Logs" 확인
2. 에러 메시지 확인
3. 주로 발생하는 문제:
   - `OPENAI_API_KEY` 환경 변수 누락
   - `requirements.txt` 오타
   - Python 버전 불일치

### 뉴스가 안 나올 때
1. Render Logs에서 에러 확인
2. OpenAI API 크레딧 잔액 확인
3. 5-10분 정도 기다려보기 (첫 수집 시간)

### API 비용이 너무 많이 나올 때
`news_classifier_gpt.py` 파일에서:
```python
# 분류할 뉴스 개수 줄이기
news_to_classify = news_items[:30]  # 30 → 10으로 변경
```

---

## 💡 추가 최적화 팁

### 1. 자동 슬립 방지 (무료 플랜)
Render 무료 플랜은 15분간 활동이 없으면 슬립 모드로 전환됩니다.
해결 방법:
- UptimeRobot (https://uptimerobot.com) 사용
- 5분마다 자동으로 사이트 핑 설정

### 2. 커스텀 도메인 연결 (선택)
- Render에서 커스텀 도메인 설정 가능
- 예: `news.mydomain.com`

### 3. HTTPS 자동 지원
- Render는 자동으로 HTTPS 인증서 제공
- 추가 설정 불필요!

---

## 📊 배포 후 체크리스트

- [ ] OpenAI API Key 정상 작동 확인
- [ ] 뉴스 수집 정상 작동 확인
- [ ] 카테고리 분류 정상 작동 확인
- [ ] 모바일에서 접속 확인
- [ ] 새로고침 버튼 작동 확인
- [ ] API 비용 모니터링 설정

---

## 🎉 완료!

이제 언제 어디서나 모바일로 실시간 뉴스를 확인할 수 있습니다!

**접속 URL**: `https://your-app-name.onrender.com`

---

## 📞 도움이 필요하면?

1. Render 공식 문서: https://render.com/docs
2. OpenAI API 문서: https://platform.openai.com/docs
3. GitHub 이슈에 질문 남기기

**Happy News Reading! 📰✨**
