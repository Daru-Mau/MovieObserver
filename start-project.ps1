# Project Startup Script for MovieObserver
# PowerShell script to start both backend and frontend servers

# Function to check if a command exists
function Test-Command {
    param (
        [string]$Command
    )
    return [bool](Get-Command -Name $Command -ErrorAction SilentlyContinue)
}

# Function to activate the virtual environment
function Activate-Environment {
    Write-Host "Activating virtual environment..." -ForegroundColor Cyan
    if (Test-Path ".\venv\Scripts\Activate.ps1") {
        & ".\venv\Scripts\Activate.ps1"
        return $true
    } else {
        Write-Host "Error: Virtual environment not found at .\venv" -ForegroundColor Red
        return $false
    }
}

# Function to start the backend server
function Start-Backend {
    Write-Host "Starting backend server..." -ForegroundColor Green
    
    Set-Location -Path ".\backend"
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Gray
    
    if (Test-Command "uvicorn") {
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m uvicorn api.main:app --reload"
        Write-Host "Backend server started. API available at http://localhost:8000" -ForegroundColor Green
    } else {
        Write-Host "Error: uvicorn not found. Make sure you have activated the virtual environment and installed the dependencies." -ForegroundColor Red
        return $false
    }
    
    Set-Location -Path ".."
    return $true
}

# Function to start the frontend server
function Start-Frontend {
    Write-Host "Starting frontend server..." -ForegroundColor Green
    
    Set-Location -Path ".\frontend"
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Gray
    
    if (Test-Command "npm") {
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev"
        Write-Host "Frontend server started. App available at http://localhost:3000" -ForegroundColor Green
    } else {
        Write-Host "Error: npm not found. Make sure you have Node.js installed." -ForegroundColor Red
        return $false
    }
    
    Set-Location -Path ".."
    return $true
}

# Main script execution
Clear-Host
Write-Host "=== MovieObserver Project Startup ===" -ForegroundColor Yellow

# Check if we're in the right directory
if (-not (Test-Path ".\backend") -or -not (Test-Path ".\frontend")) {
    Write-Host "Error: Please run this script from the root of the MovieObserver project" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
if (-not (Activate-Environment)) {
    Write-Host "Failed to activate virtual environment. Exiting." -ForegroundColor Red
    exit 1
}

# Start backend server
if (-not (Start-Backend)) {
    Write-Host "Failed to start backend server. Exiting." -ForegroundColor Red
    exit 1
}

# Start frontend server
if (-not (Start-Frontend)) {
    Write-Host "Failed to start frontend server. Exiting." -ForegroundColor Red
    exit 1
}

Write-Host "=== MovieObserver servers are running ===" -ForegroundColor Yellow
Write-Host "Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend App: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C in the server terminal windows to stop the servers" -ForegroundColor Gray
