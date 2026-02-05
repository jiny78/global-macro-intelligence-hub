@echo off
chcp 65001 > nul
color 0A

echo.
echo ════════════════════════════════════════════════════════════════
echo    🎯 Global Macro Intelligence Hub - 자동 실행기
echo ════════════════════════════════════════════════════════════════
echo.

REM 프로젝트 디렉토리로 이동
cd /d "%~dp0"
echo [1/4] 📂 프로젝트 폴더: %CD%
echo.

REM Python 설치 확인
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되어 있지 않습니다!
    echo.
    echo Python 설치 방법:
    echo 1. https://www.python.org/downloads/ 방문
    echo 2. Python 최신 버전 다운로드
    echo 3. 설치 시 "Add Python to PATH" 체크
    echo.
    pause
    exit /b 1
)

python --version
echo ✅ Python 설치 확인 완료
echo.

REM 가상환경 확인 및 생성
echo [2/4] 🔧 가상환경 확인 중...
if not exist "venv\" (
    echo ⚠️  가상환경이 없습니다. 새로 생성합니다...
    echo.
    python -m venv venv
    if errorlevel 1 (
        echo ❌ 가상환경 생성 실패!
        pause
        exit /b 1
    )
    echo ✅ 가상환경 생성 완료
) else (
    echo ✅ 가상환경 발견
)
echo.

REM 가상환경 활성화
echo [3/4] 🚀 가상환경 활성화 중...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 가상환경 활성화 실패!
    pause
    exit /b 1
)
echo ✅ 가상환경 활성화 완료
echo.

REM pip 업그레이드 (조용히)
python -m pip install --upgrade pip --quiet

REM 패키지 설치/동기화
echo [4/4] 📦 패키지 설치 및 동기화 중...
echo     (처음 실행 시 2-3분 소요됩니다)
echo.
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ⚠️  일부 패키지 설치 중 문제가 발생했습니다.
    echo     하지만 계속 진행합니다...
    echo.
)
echo ✅ 패키지 동기화 완료
echo.

REM .env 파일 확인
if not exist ".env" (
    echo ⚠️  경고: .env 파일이 없습니다!
    echo.
    echo API 키 설정이 필요합니다:
    echo 1. .env.example을 복사하여 .env 파일 생성
    echo 2. 다음 API 키를 입력:
    echo    - DART_API_KEY
    echo    - NEWS_API_KEY
    echo    - ANTHROPIC_API_KEY
    echo.
    echo 그래도 앱은 실행됩니다...
    timeout /t 3 > nul
    echo.
)

echo ════════════════════════════════════════════════════════════════
echo    ✅ 모든 준비 완료! 대시보드를 시작합니다...
echo ════════════════════════════════════════════════════════════════
echo.
echo 💡 팁:
echo    - 브라우저가 자동으로 열립니다 (http://localhost:8501)
echo    - 종료하려면 이 창에서 Ctrl+C를 누르세요
echo.
echo ════════════════════════════════════════════════════════════════
echo.

timeout /t 2 > nul

REM Streamlit 실행
streamlit run app.py

REM 종료 시 메시지
echo.
echo ════════════════════════════════════════════════════════════════
echo    🛑 대시보드가 종료되었습니다
echo ════════════════════════════════════════════════════════════════
echo.

pause
