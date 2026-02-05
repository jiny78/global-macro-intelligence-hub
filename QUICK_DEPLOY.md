# 빠른 배포 가이드 (가장 쉬운 방법)

## Option 1: GitHub Desktop 사용 (가장 쉬움)

### 1. GitHub Desktop 설치
- [desktop.github.com](https://desktop.github.com/) 다운로드
- 설치 후 GitHub 계정으로 로그인

### 2. 프로젝트 추가
1. GitHub Desktop 열기
2. "File" → "Add Local Repository" 클릭
3. "Choose..." 클릭하여 이 폴더 선택:
   ```
   C:\Users\User\Projects\Global Macro Intelligence Hub
   ```
4. "Initialize Git Repository" 클릭 (없다고 나오면)

### 3. 첫 커밋
1. Summary에 "Initial commit" 입력
2. "Commit to main" 버튼 클릭

### 4. GitHub에 발행
1. "Publish repository" 버튼 클릭
2. Name: `global-macro-intelligence-hub`
3. "Keep this code private" 체크 해제 (공개)
4. "Publish Repository" 클릭

✅ **GitHub에 업로드 완료!**

---

## Option 2: GitHub 웹에서 직접 업로드 (Desktop 없이)

### 1. GitHub 레포지토리 생성
1. [github.com/new](https://github.com/new) 접속
2. Repository name: `global-macro-intelligence-hub`
3. Public 선택
4. "Create repository" 클릭

### 2. 파일 업로드
1. "uploading an existing file" 클릭
2. 프로젝트 폴더의 모든 파일을 드래그 앤 드롭
3. 제외할 파일: `.env`, `venv/`, `data/`, `__pycache__/`
4. "Commit changes" 클릭

✅ **업로드 완료!**

---

## 다음 단계: Streamlit Cloud 배포

### 1. Streamlit Cloud 접속
[share.streamlit.io](https://share.streamlit.io/)

### 2. GitHub로 로그인
"Sign in with GitHub" 클릭

### 3. 새 앱 배포
1. "New app" 클릭
2. Repository: `YOUR_USERNAME/global-macro-intelligence-hub`
3. Branch: `main`
4. Main file: `streamlit_app.py`
5. "Deploy" 클릭

### 4. API 키 설정
1. 배포 페이지에서 "Manage app" → "Settings"
2. "Secrets" 탭 클릭
3. 다음 입력:

```toml
ANTHROPIC_API_KEY = "sk-ant-your-actual-key"
DART_API_KEY = "your-dart-key"

# Optional (이메일 기능용)
SENDER_EMAIL = "your-email@gmail.com"
APP_PASSWORD = "your-app-password"
RECIPIENT_EMAIL = "recipient@gmail.com"
```

4. "Save" 클릭
5. 앱 자동 재시작

---

## ✅ 완료!

앱 URL: `https://YOUR-USERNAME-global-macro-intelligence-hub.streamlit.app`

이 URL을 친구들과 공유하세요!

---

## 문제 해결

### "API key not found" 에러
→ Streamlit Secrets 설정 확인

### "Module not found" 에러
→ requirements.txt 확인

### 한글 깨짐
→ 이미 해결됨 (emoji 제거)

### 앱이 느림
→ 정상입니다 (무료 플랜 1GB RAM)

---

도움이 필요하면 DEPLOYMENT_GUIDE.md를 참고하세요!
