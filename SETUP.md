# 🚀 빠른 설치 가이드

## 1단계: 바탕화면 바로가기 만들기

### 방법 A: 자동 생성 (권장)

```batch
# 프로젝트 폴더에서 실행
create_desktop_shortcut.bat
```

또는 PowerShell:

```powershell
# 관리자 권한 불필요
.\create_desktop_shortcut.ps1
```

### 방법 B: 수동 생성

1. `run_analyzer.bat` 파일을 **우클릭**
2. **"바로 가기 만들기"** 선택
3. 생성된 바로가기를 **바탕화면으로 이동**
4. (선택) 이름을 "Global Macro Intelligence Hub"로 변경

---

## 2단계: 실행

### 바탕화면에서 실행

바탕화면의 **"Global Macro Intelligence Hub"** 아이콘을 **더블클릭**

### 또는 프로젝트 폴더에서 실행

```batch
run_analyzer.bat
```

---

## 📋 실행 시 자동으로 처리되는 작업

`run_analyzer.bat`가 다음을 자동으로 수행합니다:

### ✅ 1. Python 설치 확인
- Python 설치 여부 확인
- 미설치 시 안내 메시지 표시

### ✅ 2. 가상환경 확인/생성
- `venv` 폴더가 없으면 자동 생성
- 있으면 기존 환경 사용

### ✅ 3. 패키지 동기화
- `requirements.txt`를 읽어서
- 필요한 모든 패키지 자동 설치/업데이트
- 첫 실행 시 2-3분 소요

### ✅ 4. 환경변수 확인
- `.env` 파일 존재 여부 확인
- 없으면 경고 메시지 (앱은 실행됨)

### ✅ 5. 대시보드 실행
- Streamlit 앱 자동 시작
- 브라우저가 자동으로 열림 (`http://localhost:8501`)

---

## 🎯 첫 실행 체크리스트

### 필수 사항

- [x] Python 3.8 이상 설치
- [x] `run_analyzer.bat` 더블클릭

### 선택 사항 (API 키 설정)

분석 기능을 사용하려면 API 키가 필요합니다:

1. `.env.example`을 복사하여 `.env` 파일 생성
2. 다음 API 키 입력:
   ```env
   DART_API_KEY=your-key-here
   NEWS_API_KEY=your-key-here
   ANTHROPIC_API_KEY=your-key-here
   ```

---

## 💻 터미널 메시지 이해하기

### 정상 실행 예시

```
════════════════════════════════════════════════════════════════
   🎯 Global Macro Intelligence Hub - 자동 실행기
════════════════════════════════════════════════════════════════

[1/4] 📂 프로젝트 폴더: C:\Users\User\Projects\Global Macro...
Python 3.11.0
✅ Python 설치 확인 완료

[2/4] 🔧 가상환경 확인 중...
✅ 가상환경 발견

[3/4] 🚀 가상환경 활성화 중...
✅ 가상환경 활성화 완료

[4/4] 📦 패키지 설치 및 동기화 중...
     (처음 실행 시 2-3분 소요됩니다)
✅ 패키지 동기화 완료

════════════════════════════════════════════════════════════════
   ✅ 모든 준비 완료! 대시보드를 시작합니다...
════════════════════════════════════════════════════════════════

💡 팁:
   - 브라우저가 자동으로 열립니다 (http://localhost:8501)
   - 종료하려면 이 창에서 Ctrl+C를 누르세요
```

---

## 🔧 문제 해결

### Python이 설치되어 있지 않습니다

**증상:**
```
❌ Python이 설치되어 있지 않습니다!
```

**해결:**
1. https://www.python.org/downloads/ 방문
2. 최신 버전 다운로드
3. 설치 시 **"Add Python to PATH"** 반드시 체크
4. 설치 후 컴퓨터 재시작

---

### 가상환경 생성/활성화 실패

**증상:**
```
❌ 가상환경 생성 실패!
```

**해결:**
```batch
# 수동으로 생성
python -m venv venv

# 수동으로 활성화
venv\Scripts\activate
```

---

### 패키지 설치 실패

**증상:**
```
⚠️ 일부 패키지 설치 중 문제가 발생했습니다.
```

**해결:**
```batch
# 가상환경 활성화 후
venv\Scripts\activate

# 수동 설치
pip install -r requirements.txt --verbose
```

---

### 포트가 이미 사용 중

**증상:**
```
OSError: [Errno 98] Address already in use
```

**해결:**
```batch
# 다른 포트로 실행
streamlit run app.py --server.port 8502
```

또는 기존 Streamlit 프로세스 종료

---

### .env 파일이 없습니다

**증상:**
```
⚠️ 경고: .env 파일이 없습니다!
```

**해결:**
```batch
# .env.example 복사
copy .env.example .env

# 메모장으로 열어서 API 키 입력
notepad .env
```

---

## 🎓 사용 팁

### 1. 바탕화면에서 한 번에 실행
- 더블클릭만으로 모든 것이 준비됨
- 첫 실행: 2-3분
- 이후 실행: 10초

### 2. 종료 방법
- 터미널 창에서 `Ctrl+C`
- 또는 터미널 창 닫기

### 3. 업데이트 확인
- `run_analyzer.bat` 실행 시
- 자동으로 패키지 동기화됨

### 4. 여러 프로젝트 관리
- 각 프로젝트마다 별도 `run_analyzer.bat`
- 바탕화면에 여러 바로가기 생성 가능

---

## 📁 파일 구조

```
C:\Users\User\Projects\Global Macro Intelligence Hub\
│
├── run_analyzer.bat ⭐              # 메인 실행 파일
├── create_desktop_shortcut.bat     # 바로가기 생성 (배치)
├── create_desktop_shortcut.ps1     # 바로가기 생성 (PowerShell)
│
├── app.py                           # 메인 앱
├── screener.py                      # 스크리너
├── data_collector.py                # 데이터 수집
├── main.py                          # CLI 도구
│
├── venv\                            # 가상환경 (자동 생성)
├── .env                             # API 키 (직접 생성)
└── requirements.txt                 # 패키지 목록
```

---

## 🚀 다음 단계

1. ✅ 바로가기 생성
2. ✅ 첫 실행
3. ✅ 브라우저에서 앱 확인
4. ⬜ API 키 설정 (선택)
5. ⬜ 스크리닝 실행
6. ⬜ 종목 분석

---

## 📞 도움이 필요하신가요?

- **설치 문제**: SETUP.md (이 파일)
- **사용 방법**: USAGE.md
- **빠른 시작**: QUICKSTART.md
- **전체 문서**: README.md

---

**Happy Trading! 📈**
