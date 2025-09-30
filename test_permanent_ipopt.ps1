# Test IPOPT PATH Installation
Write-Host "Testing Permanent IPOPT Installation" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Test if IPOPT is available
Write-Host "Testing if ipopt.exe is accessible..." -ForegroundColor Cyan
try {
    $ipoptLocation = Get-Command ipopt.exe -ErrorAction Stop
    Write-Host "✅ IPOPT found: $($ipoptLocation.Source)" -ForegroundColor Green
    
    # Test version
    $version = ipopt.exe --version 2>&1 | Select-String "Ipopt" | Select-Object -First 1
    Write-Host "✅ Version: $version" -ForegroundColor Green
    
} catch {
    Write-Host "❌ IPOPT not accessible in PATH" -ForegroundColor Red
}

# Test with Pyomo
Write-Host ""
Write-Host "Testing IPOPT with Pyomo..." -ForegroundColor Cyan
try {
    $result = python -c "import pyomo.environ as pyo; opt = pyo.SolverFactory('ipopt'); print(f'Available: {opt.available()}'); print(f'Path: {opt.executable()}')" 2>&1
    
    if ($result -like "*Available: True*") {
        Write-Host "✅ Pyomo integration working!" -ForegroundColor Green
        $result -split "`n" | ForEach-Object { 
            if ($_ -ne "") { Write-Host "   $_" -ForegroundColor Green }
        }
    } else {
        Write-Host "❌ Pyomo integration failed" -ForegroundColor Red
        Write-Host "   $result" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Python/Pyomo test failed" -ForegroundColor Red
}

# Check environment variables
Write-Host ""
Write-Host "Checking PATH environment variables..." -ForegroundColor Cyan
$ipoptPath = "$PWD\ipopt_solver\Ipopt-3.14.16-win64-msvs2019-md\bin"
$userPath = [Environment]::GetEnvironmentVariable("PATH", "User")

if ($userPath -like "*$ipoptPath*") {
    Write-Host "✅ Found in USER PATH - will persist across sessions" -ForegroundColor Green
} else {
    Write-Host "❌ Not found in USER PATH" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎉 Test Complete! Your IPOPT installation should now be permanent." -ForegroundColor Green