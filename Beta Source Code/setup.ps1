Write-Host "`n[ EZ PyInstaller Setup ]`n" -ForegroundColor Magenta

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python not found. Downloading installer..." -ForegroundColor Cyan
    $installer = "$env:TEMP\python_installer.exe"
    Invoke-WebRequest "https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe" -OutFile $installer
    Start-Process $installer -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
    Remove-Item $installer
    Write-Host "Python installed and added to PATH." -ForegroundColor Green
} else {
    Write-Host "Python is already installed." -ForegroundColor Green
}

$pip = Get-Command pip -ErrorAction SilentlyContinue
if (-not $pip) {
    Write-Host "Installing pip..." -ForegroundColor Cyan
    python -m ensurepip
    python -m pip install --upgrade pip
}

Write-Host "Installing PyInstaller..." -ForegroundColor Cyan
python -m pip install pyinstaller

$pyi = Get-Command pyinstaller -ErrorAction SilentlyContinue
if ($pyi) {
    Write-Host "`nSetup Complete. Ready to build EXEs." -ForegroundColor Magenta
} else {
    Write-Host "`nSetup Failed. Try restarting and running again." -ForegroundColor Red
}
