# MovieObserver Setup Script

# Create virtual environment if it doesn't exist
if (-not (Test-Path ".\movieobserver-env")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv movieobserver-env
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
. .\movieobserver-env\Scripts\Activate.ps1

# Install backend dependencies
Write-Host "Installing backend dependencies..." -ForegroundColor Yellow
cd .\MovieObserver\backend
pip install -r requirements.txt

# Create .env file if it doesn't exist
if (-not (Test-Path ".\.env")) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item .\.env.example .\.env
}

# Return to root directory
cd ..\..

# Install frontend dependencies
Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
cd .\MovieObserver\frontend
npm install

# Create .env.local file if it doesn't exist
if (-not (Test-Path ".\.env.local")) {
    Write-Host "Creating .env.local file..." -ForegroundColor Yellow
    Set-Content .\.env.local "NEXT_PUBLIC_API_URL=http://localhost:8000"
}

# Return to root directory
cd ..\..

Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To start the backend (in a separate terminal):" -ForegroundColor Cyan
Write-Host "  1. Activate the virtual environment: .\movieobserver-env\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "  2. Run: cd .\MovieObserver\backend" -ForegroundColor Cyan
Write-Host "  3. Run: uvicorn api.main:app --reload" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the frontend (in a separate terminal):" -ForegroundColor Cyan
Write-Host "  1. Run: cd .\MovieObserver\frontend" -ForegroundColor Cyan
Write-Host "  2. Run: npm run dev" -ForegroundColor Cyan
Write-Host ""
Write-Host "Then open http://localhost:3000 in your browser." -ForegroundColor Cyan
