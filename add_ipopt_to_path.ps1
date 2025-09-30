# Italian CGE Model - Permanent PATH Setup Script
# This script adds IPOPT to your Windows system PATH permanently
# Run as Administrator for system-wide changes

param(
    [switch]$SystemWide = $false
)

Write-Host "========================================" -ForegroundColor Green
Write-Host "Italian CGE Model - Permanent PATH Setup" -ForegroundColor Green  
Write-Host "========================================" -ForegroundColor Green

# Get the IPOPT path
$ipoptPath = "$PWD\ipopt_solver\Ipopt-3.14.16-win64-msvs2019-md\bin"

Write-Host "IPOPT Path: $ipoptPath" -ForegroundColor Yellow

# Check if path exists
if (-not (Test-Path $ipoptPath)) {
    Write-Host "❌ IPOPT binaries not found at: $ipoptPath" -ForegroundColor Red
    Write-Host "Please ensure the IPOPT installation is complete." -ForegroundColor Red
    exit 1
}

Write-Host "✅ IPOPT binaries found" -ForegroundColor Green

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if ($SystemWide -and -not $isAdmin) {
    Write-Host "⚠️  System-wide PATH changes require Administrator privileges" -ForegroundColor Yellow
    Write-Host "Restarting script as Administrator..." -ForegroundColor Yellow
    
    # Restart as administrator
    $scriptPath = $MyInvocation.MyCommand.Path
    Start-Process PowerShell -ArgumentList "-File `"$scriptPath`" -SystemWide" -Verb RunAs
    exit
}

try {
    if ($SystemWide -and $isAdmin) {
        # Add to System PATH (requires admin)
        Write-Host "Adding IPOPT to SYSTEM PATH (all users)..." -ForegroundColor Cyan
        
        $systemPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
        
        if ($systemPath -notlike "*$ipoptPath*") {
            $newSystemPath = "$systemPath;$ipoptPath"
            [Environment]::SetEnvironmentVariable("PATH", $newSystemPath, "Machine")
            Write-Host "✅ Added IPOPT to SYSTEM PATH" -ForegroundColor Green
            Write-Host "   This will be available for all users after restart" -ForegroundColor Green
        } else {
            Write-Host "✅ IPOPT already exists in SYSTEM PATH" -ForegroundColor Green
        }
        
    } else {
        # Add to User PATH (no admin required)
        Write-Host "Adding IPOPT to USER PATH (current user only)..." -ForegroundColor Cyan
        
        $userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
        
        if ([string]::IsNullOrEmpty($userPath)) {
            $userPath = ""
        }
        
        if ($userPath -notlike "*$ipoptPath*") {
            if ($userPath -eq "") {
                $newUserPath = $ipoptPath
            } else {
                $newUserPath = "$userPath;$ipoptPath"
            }
            [Environment]::SetEnvironmentVariable("PATH", $newUserPath, "User")
            Write-Host "✅ Added IPOPT to USER PATH" -ForegroundColor Green
            Write-Host "   This will be available for current user in new sessions" -ForegroundColor Green
        } else {
            Write-Host "✅ IPOPT already exists in USER PATH" -ForegroundColor Green
        }
    }
    
    # Add to current session PATH
    if ($env:PATH -notlike "*$ipoptPath*") {
        $env:PATH = "$env:PATH;$ipoptPath"
        Write-Host "✅ Added IPOPT to current session PATH" -ForegroundColor Green
    }
    
    # Test IPOPT
    Write-Host "" 
    Write-Host "Testing IPOPT..." -ForegroundColor Cyan
    try {
        $version = & "$ipoptPath\ipopt.exe" --version 2>&1 | Select-String "Ipopt" | Select-Object -First 1
        Write-Host "✅ IPOPT is working: $version" -ForegroundColor Green
    }
    catch {
        Write-Host "⚠️  Could not test IPOPT version: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
    # Test with Python/Pyomo
    Write-Host ""
    Write-Host "Testing with Python/Pyomo..." -ForegroundColor Cyan
    try {
        $pyomoTest = python -c "import pyomo.environ as pyo; opt = pyo.SolverFactory('ipopt'); print('IPOPT available:', opt.available())" 2>&1
        Write-Host "✅ Pyomo test result: $pyomoTest" -ForegroundColor Green
    }
    catch {
        Write-Host "⚠️  Could not test with Pyomo: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "🎉 SUCCESS! IPOPT has been added to your PATH permanently!" -ForegroundColor Green
    Write-Host ""
    
    if ($SystemWide -and $isAdmin) {
        Write-Host "System-wide installation complete:" -ForegroundColor Green
        Write-Host "• Available for ALL users on this computer" -ForegroundColor Green
        Write-Host "• Will work in new PowerShell/Command Prompt sessions" -ForegroundColor Green
        Write-Host "• May require restart for some applications" -ForegroundColor Yellow
    } else {
        Write-Host "User-level installation complete:" -ForegroundColor Green
        Write-Host "• Available for current user ($env:USERNAME)" -ForegroundColor Green
        Write-Host "• Will work in new PowerShell/Command Prompt sessions" -ForegroundColor Green
        Write-Host "• No restart required" -ForegroundColor Green
        Write-Host ""
        Write-Host "To install system-wide (all users), run:" -ForegroundColor Cyan
        Write-Host "  .\add_ipopt_to_path.ps1 -SystemWide" -ForegroundColor Cyan
    }
    
    Write-Host ""
    Write-Host "Your Italian CGE model is now ready! 🚀" -ForegroundColor Green
    Write-Host "You can close this window and open a new PowerShell session." -ForegroundColor Green
    
} catch {
    Write-Host "❌ Error adding IPOPT to PATH: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Manual alternative:" -ForegroundColor Yellow
    Write-Host "1. Open System Properties (Win + R, type 'sysdm.cpl')" -ForegroundColor Yellow
    Write-Host "2. Click 'Environment Variables'" -ForegroundColor Yellow
    Write-Host "3. Under 'User variables' or 'System variables', find 'Path'" -ForegroundColor Yellow
    Write-Host "4. Click 'Edit' and add this path:" -ForegroundColor Yellow
    Write-Host "   $ipoptPath" -ForegroundColor Cyan
    exit 1
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")