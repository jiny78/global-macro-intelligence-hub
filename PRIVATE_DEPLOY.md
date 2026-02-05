# Private 배포 가이드 (1-2명 전용)

## ✅ Private 레포지토리 배포 방법

### 옵션 1: GitHub Desktop 사용 (가장 쉬움)

#### 1. GitHub Desktop 설치 및 로그인
1. [GitHub Desktop 다운로드](https://desktop.github.com/)
2. 설치 후 실행
3. "Sign in to GitHub.com" 클릭
4. 구글 계정(jiny78@gmail.com)으로 로그인

#### 2. 프로젝트 추가
1. "File" → "Add Local Repository"
2. "Choose..." → `C:\Users\User\Projects\Global Macro Intelligence Hub`
3. "Initialize Git Repository" 또는 "create a repository" 클릭

#### 3. Private 레포지토리로 발행
1. 모든 파일 선택 (체크박스)
2. Summary: "Initial commit" 입력
3. "Commit to main" 클릭
4. **"Publish repository"** 버튼 클릭
5. ⚠️ **중요**: "Keep this code private" **체크** ✅
6. Name: `global-macro-intelligence-hub`
7. "Publish Repository" 클릭

✅ **Private 레포지토리 생성 완료!**

---

### 옵션 2: 명령줄 사용

```bash
cd "C:\Users\User\Projects\Global Macro Intelligence Hub"

# Git 설정 (최초 1회)
git config --global user.email "jiny78@gmail.com"
git config --global user.name "jiny78"

# Git 초기화
git init
git add .
git commit -m "Initial commit: Private deployment"

# GitHub CLI 설치 후 (https://cli.github.com/)
gh auth login
gh repo create global-macro-intelligence-hub --private --source=. --push
```

---

## 🌐 Streamlit Cloud Private 배포

### 좋은 소식! 
Streamlit Community Cloud는 **Private 레포지토리도 지원합니다!**

#### 1. Streamlit Cloud 접속
[share.streamlit.io](https://share.streamlit.io/)

#### 2. GitHub로 로그인
"Sign in with GitHub" 클릭

#### 3. Private 레포지토리 권한 부여
- Streamlit이 Private 레포지토리 접근 권한 요청
- "Authorize streamlit" 클릭
- Private 레포지토리 선택 권한 부여

#### 4. 앱 배포
1. "New app" 클릭
2. Repository: `jiny78/global-macro-intelligence-hub` (Private 표시)
3. Branch: `main`
4. Main file: `streamlit_app.py`
5. "Deploy!" 클릭

#### 5. Secrets 설정
"Advanced settings" → "Secrets":

```toml
ANTHROPIC_API_KEY = "sk-ant-your-key"
DART_API_KEY = "your-dart-key"

# Optional
SENDER_EMAIL = "jiny78@gmail.com"
APP_PASSWORD = "your-app-password"
RECIPIENT_EMAIL = "recipient@gmail.com"
```

---

## 🔐 추가 보안: 비밀번호 보호

앱에 비밀번호 추가하려면:

### streamlit_app.py 맨 위에 추가:

```python
import streamlit as st

# 비밀번호 체크
def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "your-secret-password":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # 비밀번호 삭제
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # 첫 실행, 비밀번호 입력 요청
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # 비밀번호 틀림
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # 비밀번호 맞음
        return True

# 메인 앱 실행 전 비밀번호 체크
if not check_password():
    st.stop()  # 비밀번호 틀리면 여기서 멈춤

# 아래부터 원래 코드...
```

---

## 👥 다른 사람 초대 방법

### GitHub 레포지토리에 협업자 추가:

1. GitHub 레포지토리 페이지 접속
2. "Settings" 탭 클릭
3. 왼쪽 "Collaborators" 클릭
4. "Add people" 클릭
5. 초대할 사람의 GitHub 아이디/이메일 입력
6. 권한 선택:
   - **Read**: 앱만 사용 가능
   - **Write**: 코드 수정 가능
   - **Admin**: 모든 권한

---

## 📊 비용 (Private 배포)

| 항목 | 비용 |
|------|------|
| GitHub Private Repo | 무료 |
| Streamlit Cloud (Private) | 무료 |
| Claude API | $5-10/월 (사용량 따라) |
| **총합** | **$5-10/월** |

---

## ⚡ 배포 URL 비밀 유지

배포 후 URL은:
`https://jiny78-global-macro-intelligence-hub.streamlit.app`

- Private 레포지토리여도 **앱 URL은 누구나 접근 가능**
- 비밀번호 보호 추가 권장 (위 코드 참고)
- 또는 URL을 아는 사람만 사용

---

## 🔒 보안 체크리스트

- [x] Private 레포지토리로 설정
- [x] `.env` 파일 GitHub에 올리지 않음 (.gitignore)
- [x] API 키는 Streamlit Secrets에만 저장
- [ ] (선택) 앱에 비밀번호 보호 추가
- [ ] (선택) 특정 IP만 접근 허용 (유료 플랜)

---

## 문제 해결

### "Repository not found"
→ Streamlit에 Private 레포 권한 부여 확인

### "Access denied"
→ GitHub Settings → Applications → Streamlit 권한 재확인

### 비밀번호 보호 추가 후 에러
→ 코드 위치 확인 (맨 위에 있어야 함)

---

**준비 완료! GitHub Desktop으로 5분 안에 배포하세요.**
