# Deep Decoder - Installation Script for Windows
# Run this script in PowerShell from the project directory

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deep Decoder - Quick Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python 3.7+ first." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Ask user if they want to create virtual environment
$createVenv = Read-Host "Create virtual environment? (Recommended) [Y/n]"
if ($createVenv -ne "n" -and $createVenv -ne "N") {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    .\venv\Scripts\Activate.ps1
    
    Write-Host "✓ Virtual environment created and activated" -ForegroundColor Green
    Write-Host ""
}

# Install package
Write-Host "Installing deep-decoder package..." -ForegroundColor Yellow
pip install -e .

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Package installed successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Installation failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Ask to install dev dependencies
$installDev = Read-Host "Install development dependencies? [y/N]"
if ($installDev -eq "y" -or $installDev -eq "Y") {
    Write-Host "Installing dev dependencies..." -ForegroundColor Yellow
    pip install -e ".[dev]"
    Write-Host "✓ Dev dependencies installed" -ForegroundColor Green
    Write-Host ""
}

# Run tests
Write-Host "Running tests..." -ForegroundColor Yellow
python examples/test_package.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✓ Installation Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Quick Start:" -ForegroundColor Cyan
    Write-Host "  from deep_decoder import quick_decode" -ForegroundColor White
    Write-Host '  result = quick_decode("SGVsbG8gV29ybGQh")' -ForegroundColor White
    Write-Host '  print(result)  # Hello World!' -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Cyan
    Write-Host "  python examples/basic_usage.py" -ForegroundColor White
    Write-Host "  python examples/advanced_usage.py" -ForegroundColor White
    Write-Host ""
    Write-Host "Documentation:" -ForegroundColor Cyan
    Write-Host "  README.md - Full documentation" -ForegroundColor White
    Write-Host "  QUICKSTART.md - Quick start guide" -ForegroundColor White
    Write-Host "  INSTALL.md - Installation guide" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "✗ Some tests failed. Please check the output above." -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
