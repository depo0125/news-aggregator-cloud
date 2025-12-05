# 📰 실시간 뉴스 수집 시스템 (클라우드 배포용)

ChatGPT API와 Render를 활용한 실시간 뉴스 수집, 분류, 요약 웹 애플리케이션

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)

## ✨ 주요 기능

- 🔄 **실시간 뉴스 수집**: RSS 피드를 통한 자동 뉴스 수집
- 🤖 **AI 자동 분류**: ChatGPT를 활용한 정교한 카테고리 분류
- 📝 **스마트 요약**: AI 기반 뉴스 한 줄 요약
- 📱 **모바일 최적화**: 언제 어디서나 편리하게 확인
- 🔄 **자동 업데이트**: 30분마다 최신 뉴스 자동 수집
- 🌐 **클라우드 호스팅**: Render를 통한 24/7 운영

## 📂 프로젝트 구조

```
news-aggregator-cloud/
├── app.py                      # Flask 메인 서버
├── news_collector.py           # 뉴스 수집 모듈
├── news_classifier_gpt.py      # ChatGPT 분류 모듈
├── requirements.txt            # Python 패키지
├── Procfile                    # Render 배포 설정
├── runtime.txt                 # Python 버전
├── static/
│   └── index.html             # 프론트엔드 (React)
├── .env.example               # 환경 변수 예시
├── .gitignore                 # Git 제외 파일
└── DEPLOYMENT_GUIDE.md        # 배포 가이드
```

## 🚀 빠른 시작

### 로컬 실행 (테스트용)

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. 환경 변수 설정
cp .env.example .env
# .env 파일에 OPENAI_API_KEY 입력

# 3. 서버 실행
python app.py

# 4. 브라우저에서 접속
http://localhost:5000
```

### 클라우드 배포 (프로덕션)

**[📘 상세한 배포 가이드 보기](DEPLOYMENT_GUIDE.md)**

간단 요약:
1. GitHub에 코드 업로드
2. Render에서 웹 서비스 생성
3. OpenAI API Key 환경 변수 설정
4. 자동 배포 완료!

## 💰 비용

### 무료
- GitHub 호스팅: $0
- Render 서버: $0 (월 750시간 무료)

### 유료
- **OpenAI API**: 월 $3-10
  - GPT-4o-mini 모델 사용
  - 하루 100개 뉴스 분류 기준
  - 사용량 기반 과금

**총 예상 비용**: 월 $3-10

## 📱 모바일 사용

### 홈 화면에 추가

**iOS (Safari)**
1. 사이트 접속
2. 공유 버튼 → "홈 화면에 추가"

**Android (Chrome)**
1. 사이트 접속
2. 메뉴 → "홈 화면에 추가"

이제 앱처럼 사용 가능! 📱

## 🔧 설정

### 뉴스 수집 주기 변경

`app.py` 파일에서:
```python
time.sleep(1800)  # 1800초 = 30분
```

### 분류할 뉴스 개수 조절 (비용 절감)

`app.py` 파일에서:
```python
news_to_classify = news_items[:30]  # 30개 → 원하는 개수로 변경
```

### RSS 피드 추가

`news_collector.py` 파일의 `rss_feeds` 딕셔너리 수정

## 🎨 카테고리

- 🏛️ **정치/정책**: 정부, 국회, 정당 관련 뉴스
- 🚨 **사건/사고**: 범죄, 재난, 사건사고
- 💰 **경제/주식**: 경제지표, 기업, 주식시장
- 🏠 **부동산**: 아파트, 주택, 부동산 정책
- 🌍 **글로벌**: 국제 뉴스 (미국 제외)
- 🇺🇸 **미국**: 미국 관련 뉴스
- 📌 **기타**: 기타 뉴스

## 🔒 보안

- `.env` 파일은 절대 Git에 커밋하지 않기
- OpenAI API Key는 환경 변수로만 관리
- Render에서 환경 변수 암호화 저장

## 📊 모니터링

### OpenAI API 사용량 확인
1. https://platform.openai.com/usage 접속
2. 일별/월별 사용량 확인
3. 사용 한도 설정 가능

### Render 로그 확인
1. Render 대시보드
2. "Logs" 탭
3. 실시간 서버 로그 확인

## 🐛 문제 해결

### 뉴스가 수집되지 않음
- Render Logs 확인
- RSS 피드 URL 유효성 검사
- 네트워크 연결 확인

### AI 분류가 작동하지 않음
- OpenAI API Key 확인
- API 크레딧 잔액 확인
- 자동으로 키워드 기반 분류로 전환됨

### 배포가 실패함
- `requirements.txt` 확인
- Python 버전 확인 (`runtime.txt`)
- 환경 변수 설정 확인

## 🔄 업데이트

### 코드 수정 후 재배포

```bash
# Git에 변경사항 커밋
git add .
git commit -m "Update news sources"
git push

# Render에서 자동으로 재배포됨!
```

## 🌟 향후 계획

- [ ] 사용자 맞춤 키워드 알림
- [ ] 북마크/즐겨찾기 기능
- [ ] 뉴스 감성 분석
- [ ] 트렌드 분석 차트
- [ ] 다크 모드
- [ ] PWA 변환
- [ ] 푸시 알림

## 📝 라이선스

MIT License

## 🤝 기여

Pull Request를 환영합니다!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 문의

이슈가 있으시면 GitHub Issues에 남겨주세요!

---

**Made with ❤️ and 🤖 AI**

⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요!
