# Test IPOPT PATH Installation
# This script tests if IPOPT is permanently available in new sessions

Write-Host "========================================" -ForegroundColor Green
Write-Host "Testing Permanent IPOPT Installation" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Test 1: Check if IPOPT is in PATH
Write-Host "Test 1: Checking if ipopt.exe is in PATH..." -ForegroundColor Cyan
try {
    $ipoptLocation = Get-Command ipopt.exe -ErrorAction Stop
    Write-Host "✅ IPOPT found in PATH: $($ipoptLocation.Source)" -ForegroundColor Green
} catch {
    Write-Host "❌ IPOPT not found in PATH" -ForegroundColor Red
    
    # Check user PATH environment variable
    $userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    $ipoptPath = "$PWD\ipopt_solver\Ipopt-3.14.16-win64-msvs2019-md\bin"
    
    if ($userPath -like "*$ipoptPath*") {
        Write-Host "⚠️  IPOPT is in USER PATH but not available in current session" -ForegroundColor Yellow
        Write-Host "   Please restart PowerShell or run: refreshenv" -ForegroundColor Yellow
    } else {
        Write-Host "❌ IPOPT not found in USER PATH either" -ForegroundColor Red
    }
}

# Test 2: Test IPOPT version
Write-Host ""
Write-Host "Test 2: Testing IPOPT functionality..." -ForegroundColor Cyan
try {
    $version = ipopt.exe --version 2>&1 | Select-String "Ipopt" | Select-Object -First 1
    Write-Host "✅ IPOPT version: $version" -ForegroundColor Green
} catch {
    Write-Host "❌ Cannot run IPOPT: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Test with Python/Pyomo
Write-Host ""
Write-Host "Test 3: Testing IPOPT with Pyomo..." -ForegroundColor Cyan
try {
    $pyomoResult = python -c "import pyomo.environ as pyo; opt = pyo.SolverFactory('ipopt'); print('Available:', opt.available()); print('Path:', opt.executable())" 2>&1
    if ($pyomoResult -like "*Available: True*") {
        Write-Host "✅ Pyomo can use IPOPT:" -ForegroundColor Green
        $pyomoResult -split "`n" | ForEach-Object { Write-Host "   $_" -ForegroundColor Green }
    } else {
        Write-Host "❌ Pyomo cannot use IPOPT:" -ForegroundColor Red
        Write-Host "   $pyomoResult" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Error testing with Pyomo: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Environment variables
Write-Host ""
Write-Host "Test 4: Checking environment variables..." -ForegroundColor Cyan
$userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
$systemPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
$ipoptPath = "$PWD\ipopt_solver\Ipopt-3.14.16-win64-msvs2019-md\bin"

Write-Host "IPOPT target path: $ipoptPath" -ForegroundColor Yellow

if ($userPath -like "*$ipoptPath*") {
    Write-Host "✅ Found in USER PATH" -ForegroundColor Green
} else {
    Write-Host "❌ Not found in USER PATH" -ForegroundColor Red
}

if ($systemPath -like "*$ipoptPath*") {
    Write-Host "✅ Found in SYSTEM PATH" -ForegroundColor Green
} else {
    Write-Host "⚠️  Not found in SYSTEM PATH (run with -SystemWide for all users)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Installation Status Summary" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Overall status
$allGood = $true
try {
    $null = Get-Command ipopt.exe -ErrorAction Stop
    $pyomoTest = python -c "import pyomo.environ as pyo; print(pyo.SolverFactory('ipopt').available())" 2>&1
    if ($pyomoTest -like "*True*") {
        Write-Host "🎉 PERFECT! IPOPT is fully functional and permanent!" -ForegroundColor Green
        Write-Host "   • Available in PATH" -ForegroundColor Green
        Write-Host "   • Works with Pyomo" -ForegroundColor Green
        Write-Host "   • Will persist across sessions" -ForegroundColor Green
        Write-Host ""
        Write-Host "Your Italian CGE model is ready to run! 🇮🇹📊" -ForegroundColor Green
    } else {
        $allGood = $false
    }
} catch {
    $allGood = $false
}

if (-not $allGood) {
    Write-Host "⚠️  Installation needs attention" -ForegroundColor Yellow
    Write-Host "   Try restarting PowerShell or running:" -ForegroundColor Yellow
    Write-Host "   .\add_ipopt_to_path.ps1" -ForegroundColor Cyan
}

Write-Host ""