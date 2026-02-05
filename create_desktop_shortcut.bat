@echo off
chcp 65001 > nul
echo.
echo ════════════════════════════════════════════════════════════════
echo    바탕화면 바로가기 생성
echo ════════════════════════════════════════════════════════════════
echo.

REM 현재 디렉토리
set "PROJECT_DIR=%~dp0"
set "BAT_FILE=%PROJECT_DIR%run_analyzer.bat"
set "DESKTOP=%USERPROFILE%\Desktop"
set "SHORTCUT_NAME=Global Macro Intelligence Hub.lnk"

REM VBS 스크립트로 바로가기 생성
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = "%DESKTOP%\%SHORTCUT_NAME%" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "%BAT_FILE%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%PROJECT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "Global Macro Intelligence Hub - AI 주식 분석" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.IconLocation = "%%SystemRoot%%\System32\SHELL32.dll,13" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"

REM VBS 실행
cscript //nologo "%TEMP%\CreateShortcut.vbs"

REM 임시 파일 삭제
del "%TEMP%\CreateShortcut.vbs"

if exist "%DESKTOP%\%SHORTCUT_NAME%" (
    echo ✅ 바로가기가 바탕화면에 생성되었습니다!
    echo.
    echo 📍 위치: %DESKTOP%\%SHORTCUT_NAME%
    echo.
    echo 이제 바탕화면에서 "Global Macro Intelligence Hub" 아이콘을
    echo 더블클릭하여 실행할 수 있습니다.
) else (
    echo ❌ 바로가기 생성 실패
    echo.
    echo 수동으로 생성하는 방법:
    echo 1. run_analyzer.bat 파일을 우클릭
    echo 2. "바로 가기 만들기" 선택
    echo 3. 생성된 바로가기를 바탕화면으로 이동
)

echo.
echo ════════════════════════════════════════════════════════════════
echo.
pause
