@echo off
setlocal

REM Run backend + frontend for local Windows development.
REM Usage: double-click this file or run `run-local-windows.bat` from the repo root.

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo [ERROR] Python virtual environment not found at .venv\Scripts\python.exe
  echo Create it first:
  echo   py -m venv .venv
  echo   .venv\Scripts\activate
  echo   pip install -r requirements.txt
  exit /b 1
)

if not exist "frontend\node_modules" (
  echo [INFO] frontend\node_modules not found. Installing frontend dependencies...
  pushd frontend
  call npm install
  if errorlevel 1 (
    echo [ERROR] npm install failed.
    popd
    exit /b 1
  )
  popd
)

echo Starting backend on http://localhost:8000 ...
start "ResearchHub Backend" cmd /k "cd /d %~dp0 && .venv\Scripts\activate && uvicorn app.main:app --reload --port 8000"

echo Starting frontend on http://localhost:3000 ...
start "ResearchHub Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo Done. Two new terminal windows were opened.
endlocal
