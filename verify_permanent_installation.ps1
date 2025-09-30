# Final Verification Script
# Run this to test IPOPT permanency

Write-Host "Final IPOPT Installation Verification" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""

Write-Host "Current session test:" -ForegroundColor Cyan
Write-Host "1. IPOPT command test:" -ForegroundColor Yellow
ipopt.exe --version | Select-String "Ipopt"

Write-Host ""
Write-Host "2. Python/Pyomo test:" -ForegroundColor Yellow
python -c "import pyomo.environ as pyo; print('IPOPT available:', pyo.SolverFactory('ipopt').available())"

Write-Host ""
Write-Host "3. Environment variable check:" -ForegroundColor Yellow
$userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
$ipoptPath = "$PWD\ipopt_solver\Ipopt-3.14.16-win64-msvs2019-md\bin"

if ($userPath -like "*$ipoptPath*") {
    Write-Host "✅ IPOPT path found in USER environment variables" -ForegroundColor Green
    Write-Host "   This means IPOPT will be available in NEW sessions!" -ForegroundColor Green
} else {
    Write-Host "❌ IPOPT path NOT found in USER environment variables" -ForegroundColor Red
}

Write-Host ""
Write-Host "To verify permanency:" -ForegroundColor Cyan
Write-Host "1. Close this PowerShell window" -ForegroundColor White
Write-Host "2. Open a NEW PowerShell window" -ForegroundColor White  
Write-Host "3. Navigate to this directory" -ForegroundColor White
Write-Host "4. Run: ipopt.exe --version" -ForegroundColor White
Write-Host "5. If it works, installation is permanent! 🎉" -ForegroundColor Green

Write-Host ""
Write-Host "Your Italian CGE model environment is ready!" -ForegroundColor Green