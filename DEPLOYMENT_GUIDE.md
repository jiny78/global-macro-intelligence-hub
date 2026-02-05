# Streamlit Cloud 배포 가이드

## 단계별 배포 방법

### 1. GitHub 레포지토리 생성

1. [github.com](https://github.com)에 로그인
2. 우측 상단 "+" 클릭 → "New repository"
3. Repository name: `global-macro-intelligence-hub` (또는 원하는 이름)
4. Public 또는 Private 선택
5. "Create repository" 클릭

### 2. 로컬 코드를 GitHub에 푸시

```bash
cd "C:\Users\User\Projects\Global Macro Intelligence Hub"

# Git 초기화 (이미 되어있지 않다면)
git init

# 파일 추가
git add .

# 커밋
git commit -m "Initial commit: Global Macro Intelligence Hub"

# GitHub 레포지토리 연결 (YOUR_USERNAME을 본인 GitHub 아이디로 변경)
git remote add origin https://github.com/YOUR_USERNAME/global-macro-intelligence-hub.git

# 푸시
git branch -M main
git push -u origin main
```

### 3. Streamlit Cloud 배포

1. [share.streamlit.io](https://share.streamlit.io/) 접속
2. "Sign in with GitHub" 클릭
3. GitHub 계정으로 로그인
4. "New app" 클릭
5. 다음 정보 입력:
   - **Repository**: `YOUR_USERNAME/global-macro-intelligence-hub`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
6. "Advanced settings" 클릭하여 Python 버전 확인 (3.9 이상)

### 4. Secrets 설정 (중요!)

Streamlit Cloud 배포 페이지에서:

1. "Advanced settings" 클릭
2. "Secrets" 탭 클릭
3. 다음 형식으로 입력:

```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
DART_API_KEY = "your-dart-api-key"

# Optional (이메일 기능 사용 시)
SENDER_EMAIL = "your-email@gmail.com"
APP_PASSWORD = "your-app-password"
RECIPIENT_EMAIL = "recipient@gmail.com"
```

4. "Save" 클릭
5. "Deploy!" 클릭

### 5. 배포 완료!

- 몇 분 후 앱이 배포됩니다
- URL: `https://YOUR_USERNAME-global-macro-intelligence-hub-main-streamlit-app.streamlit.app`
- 이 URL을 다른 사람과 공유하면 누구나 접속 가능!

## 주의사항

### API 키 비용

- **Anthropic Claude API**: 사용량에 따라 과금
  - Sonnet 4: Input $3/M tokens, Output $15/M tokens
  - 한 번의 분석: 약 $0.05-0.10
  - 월 예산 설정 추천: [console.anthropic.com](https://console.anthropic.com/)

- **DART API**: 완전 무료
- **yfinance**: 무료
- **Google News RSS**: 무료

### 보안

- `.env` 파일은 **절대** GitHub에 올리지 마세요
- `.gitignore`에 `.env`가 포함되어 있는지 확인
- Streamlit Cloud Secrets에만 API 키 입력

### Public vs Private Repository

**Public (공개)**:
- 장점: 누구나 코드 볼 수 있음, 포트폴리오로 활용 가능
- 단점: 코드 공개

**Private (비공개)**:
- 장점: 코드 비공개
- 단점: Streamlit Cloud 무료 플랜에서는 1개만 가능

## 업데이트 방법

코드를 수정한 후:

```bash
git add .
git commit -m "Update: describe your changes"
git push
```

Streamlit Cloud가 자동으로 재배포합니다!

## 트러블슈팅

### 문제 1: 앱이 시작되지 않음
- Streamlit Cloud 로그 확인
- `requirements.txt`에 모든 패키지가 있는지 확인
- Python 버전 확인 (3.9 이상)

### 문제 2: API 키 에러
- Secrets 설정 확인
- 키 이름이 정확한지 확인 (대소문자 구분)
- 키 앞뒤 공백 제거

### 문제 3: 한글 깨짐
- 이미 해결됨 (emoji 제거 완료)

### 문제 4: 메모리 부족
- Streamlit Cloud 무료 플랜: 1GB RAM
- 큰 데이터 처리 시 제한 가능
- 캐싱 활용 (@st.cache_data)

## 대안 배포 방법

### 1. Heroku (유료)
- 더 많은 리소스
- 데이터베이스 연동 쉬움
- 월 $7부터

### 2. AWS EC2 (복잡하지만 유연)
- 완전한 제어
- 확장 가능
- 설정 복잡

### 3. ngrok (임시 공유)
```bash
ngrok http 8501
```
- PC가 켜져 있어야 함
- 개발/테스트용

## 예상 비용 (월)

| 항목 | 비용 |
|------|------|
| Streamlit Cloud | 무료 |
| Claude API (월 100회 분석) | $5-10 |
| DART API | 무료 |
| **총합** | **$5-10** |

## 추가 기능 제안

배포 후 추가할 수 있는 기능:
- 사용자 로그인 (Streamlit Auth)
- 분석 히스토리 저장 (SQLite/PostgreSQL)
- 실시간 알림 (Discord/Telegram bot)
- 포트폴리오 추적

---

**도움이 필요하면 이슈를 열어주세요!**
