:: In the source code change the open powershell with "setup.bat" powershell works better though

@echo off
setlocal
echo.
echo [ EZ PyInstaller Setup ]
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo Python not found. Downloading installer...
    set "installer=%TEMP%\python_installer.exe"
    powershell -Command "Invoke-WebRequest 'https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe' -OutFile '%installer%'"
    start /wait "" "%installer%" /quiet InstallAllUsers=1 PrependPath=1
    del "%installer%"
    echo Python installed and added to PATH.
) else (
    echo Python is already installed.
)

python -m pip --version >nul 2>nul
if errorlevel 1 (
    echo Installing pip...
    python -m ensurepip
    python -m pip install --upgrade pip
)

echo Installing PyInstaller...
python -m pip install pyinstaller

pyinstaller --version >nul 2>nul
if errorlevel 1 (
    echo.
    echo Setup Failed. Try restarting and running again.
) else (
    echo.
    echo Setup Complete. Ready to build EXEs.
)

endlocal
pause
