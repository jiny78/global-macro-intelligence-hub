# Create Desktop Shortcut for Global Macro Intelligence Hub

$WshShell = New-Object -ComObject WScript.Shell
$Desktop = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $Desktop "Global Macro Hub.lnk"

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "C:\Users\User\Projects\Global Macro Intelligence Hub\run_analyzer.bat"
$Shortcut.WorkingDirectory = "C:\Users\User\Projects\Global Macro Intelligence Hub"
$Shortcut.Description = "Global Macro Intelligence Hub - AI Stock Analysis"
$Shortcut.IconLocation = "$env:SystemRoot\System32\SHELL32.dll,13"
$Shortcut.Save()

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Desktop Shortcut Created Successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Location: $ShortcutPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now double-click 'Global Macro Hub' on your desktop!" -ForegroundColor Yellow
Write-Host ""
