# Git Upload Script for Deep Decoder
# Run this script to upload your project to GitHub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deep Decoder - GitHub Upload Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version 2>&1
    Write-Host "✓ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Git not found! Please install Git first:" -ForegroundColor Red
    Write-Host "  https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Check if already a git repository
if (Test-Path ".git") {
    Write-Host "⚠️  Git repository already exists" -ForegroundColor Yellow
    $reinit = Read-Host "Reinitialize? This will reset git history [y/N]"
    if ($reinit -eq "y" -or $reinit -eq "Y") {
        Remove-Item -Recurse -Force .git
        Write-Host "✓ Removed existing git repository" -ForegroundColor Green
    } else {
        Write-Host "Keeping existing repository..." -ForegroundColor Yellow
        git status
        Write-Host ""
        Write-Host "To push changes:" -ForegroundColor Cyan
        Write-Host "  git add ." -ForegroundColor White
        Write-Host "  git commit -m 'Update'" -ForegroundColor White
        Write-Host "  git push" -ForegroundColor White
        exit 0
    }
}

Write-Host ""
Write-Host "Step 1: Initialize Git Repository" -ForegroundColor Cyan
Write-Host "-----------------------------------" -ForegroundColor Gray

# Initialize git
git init
Write-Host "✓ Git initialized" -ForegroundColor Green

# Create main branch
git branch -M main
Write-Host "✓ Main branch created" -ForegroundColor Green

Write-Host ""
Write-Host "Step 2: Add Files" -ForegroundColor Cyan
Write-Host "-----------------------------------" -ForegroundColor Gray

# Add all files
git add .
Write-Host "✓ Files added to staging" -ForegroundColor Green

# Show what will be committed
Write-Host ""
Write-Host "Files to be committed:" -ForegroundColor Yellow
git status --short

Write-Host ""
Write-Host "Step 3: Create Initial Commit" -ForegroundColor Cyan
Write-Host "-----------------------------------" -ForegroundColor Gray

# Commit
git commit -m "Initial commit: Deep Decoder for IDS/IPS, WAF v1.0.0"
Write-Host "✓ Initial commit created" -ForegroundColor Green

Write-Host ""
Write-Host "Step 4: Add Remote Repository" -ForegroundColor Cyan
Write-Host "-----------------------------------" -ForegroundColor Gray
Write-Host ""
Write-Host "⚠️  IMPORTANT: Create GitHub repository first!" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Go to: https://github.com/new" -ForegroundColor White
Write-Host "2. Repository name: deep-decoder" -ForegroundColor White
Write-Host "3. Description: Deep Decoder for IDS/IPS, WAF" -ForegroundColor White
Write-Host "4. Public or Private" -ForegroundColor White
Write-Host "5. DO NOT initialize with README, .gitignore, or license" -ForegroundColor Red
Write-Host "6. Click 'Create repository'" -ForegroundColor White
Write-Host ""

$createRepo = Read-Host "Have you created the GitHub repository? [y/N]"
if ($createRepo -ne "y" -and $createRepo -ne "Y") {
    Write-Host ""
    Write-Host "Please create the repository first, then run this script again." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "After creating, use:" -ForegroundColor Cyan
    Write-Host "  git remote add origin https://github.com/khoilv2005/deep-decoder.git" -ForegroundColor White
    Write-Host "  git push -u origin main" -ForegroundColor White
    exit 0
}

Write-Host ""
$repoUrl = Read-Host "Enter your GitHub repository URL (default: https://github.com/khoilv2005/deep-decoder.git)"

if ([string]::IsNullOrWhiteSpace($repoUrl)) {
    $repoUrl = "https://github.com/khoilv2005/deep-decoder.git"
}

Write-Host "Using repository: $repoUrl" -ForegroundColor White

# Add remote
git remote add origin $repoUrl
Write-Host "✓ Remote repository added" -ForegroundColor Green

Write-Host ""
Write-Host "Step 5: Push to GitHub" -ForegroundColor Cyan
Write-Host "-----------------------------------" -ForegroundColor Gray

# Push
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✓ SUCCESS!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your project is now on GitHub!" -ForegroundColor Green
    Write-Host "View it at: $($repoUrl -replace '\.git$','')" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. ✓ Uploaded to GitHub" -ForegroundColor Green
    Write-Host "2. ☐ Add topics/tags on GitHub (ids, ips, waf, security, decoder)" -ForegroundColor White
    Write-Host "3. ☐ Add description on GitHub" -ForegroundColor White
    Write-Host "4. ☐ Star your own repo 😊" -ForegroundColor White
    Write-Host "5. ☐ Share with others!" -ForegroundColor White
    Write-Host ""
    Write-Host "To update later:" -ForegroundColor Cyan
    Write-Host "  git add ." -ForegroundColor White
    Write-Host "  git commit -m 'Update description'" -ForegroundColor White
    Write-Host "  git push" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "✗ Push failed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "1. Repository doesn't exist - create it on GitHub first" -ForegroundColor White
    Write-Host "2. Authentication failed - use GitHub Personal Access Token" -ForegroundColor White
    Write-Host "3. Wrong repository URL - check the URL" -ForegroundColor White
    Write-Host ""
    Write-Host "Try manual push:" -ForegroundColor Cyan
    Write-Host "  git push -u origin main" -ForegroundColor White
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
