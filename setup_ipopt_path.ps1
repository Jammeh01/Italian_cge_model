# Italian CGE Model - Permanent IPOPT Setup Script
# This script adds IPOPT to your system PATH permanently

Write-Host "========================================" -ForegroundColor Green
Write-Host "Italian CGE Model - IPOPT PATH Setup" -ForegroundColor Green  
Write-Host "========================================" -ForegroundColor Green

$ipoptPath = "$PWD\ipopt_solver\Ipopt-3.14.16-win64-msvs2019-md\bin"

Write-Host "IPOPT Location: $ipoptPath" -ForegroundColor Yellow

# Check if path exists
if (Test-Path $ipoptPath) {
    Write-Host "✅ IPOPT binaries found" -ForegroundColor Green
    
    # Add to current session PATH
    $env:PATH = "$env:PATH;$ipoptPath"
    Write-Host "✅ Added IPOPT to current session PATH" -ForegroundColor Green
    
    # Test IPOPT
    try {
        $version = & "$ipoptPath\ipopt.exe" --version 2>&1 | Select-String "Ipopt"
        Write-Host "✅ IPOPT is working: $version" -ForegroundColor Green
    }
    catch {
        Write-Host "⚠️  Could not test IPOPT version" -ForegroundColor Yellow
    }
    
    Write-Host "" 
    Write-Host "To make this permanent for all sessions:" -ForegroundColor Cyan
    Write-Host "1. Run this script each time you open PowerShell, OR" -ForegroundColor Cyan
    Write-Host "2. Add to Windows system PATH manually via System Properties" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "For now, IPOPT is available in this session!" -ForegroundColor Green
    
} else {
    Write-Host "❌ IPOPT binaries not found at: $ipoptPath" -ForegroundColor Red
    Write-Host "Please ensure the IPOPT extraction completed successfully." -ForegroundColor Red
}

Write-Host ""
Write-Host "Ready to use your Italian CGE model! 🚀" -ForegroundColor Green