# PowerShell Script to Create Desktop Shortcut
# UTF-8 Encoding

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "   바탕화면 바로가기 생성 (PowerShell)" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# 경로 설정
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BatFile = Join-Path $ProjectDir "run_analyzer.bat"
$Desktop = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $Desktop "Global Macro Intelligence Hub.lnk"

# 바로가기 생성
try {
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = $BatFile
    $Shortcut.WorkingDirectory = $ProjectDir
    $Shortcut.Description = "Global Macro Intelligence Hub - AI 주식 분석"
    $Shortcut.IconLocation = "$env:SystemRoot\System32\SHELL32.dll,13"
    $Shortcut.Save()

    Write-Host "✅ 바로가기가 바탕화면에 생성되었습니다!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📍 위치: $ShortcutPath" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "이제 바탕화면에서 'Global Macro Intelligence Hub' 아이콘을" -ForegroundColor White
    Write-Host "더블클릭하여 실행할 수 있습니다." -ForegroundColor White
}
catch {
    Write-Host "❌ 바로가기 생성 실패: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "수동으로 생성하는 방법:" -ForegroundColor Yellow
    Write-Host "1. run_analyzer.bat 파일을 우클릭" -ForegroundColor White
    Write-Host "2. '바로 가기 만들기' 선택" -ForegroundColor White
    Write-Host "3. 생성된 바로가기를 바탕화면으로 이동" -ForegroundColor White
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
