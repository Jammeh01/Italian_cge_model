# Manual System PATH Setup Guide

## Current Status ✅
- **IPOPT** has been added to your **USER PATH** successfully
- It will be available in all new PowerShell/Command Prompt sessions for your user account
- No restart required for user-level installation

## Manual System-Wide Installation (Optional)

If you want IPOPT available for **ALL users** on this computer, follow these steps:

### Method 1: Using the PowerShell Script (Recommended)
1. **Right-click** on PowerShell and select **"Run as Administrator"**
2. Navigate to this directory:
   ```powershell
   cd "C:\Users\BAKARY JAMMEH\OneDrive - Università degli Studi di Milano-Bicocca\Desktop\MODELLING\Italian_cge_model"
   ```
3. Run:
   ```powershell
   .\add_ipopt_to_path.ps1 -SystemWide
   ```

### Method 2: Manual GUI Method
1. **Press `Win + R`** and type `sysdm.cpl`, press Enter
2. Click **"Environment Variables"** button
3. In the **"System variables"** section (bottom), find and select **"Path"**
4. Click **"Edit"**
5. Click **"New"**
6. Add this path:
   ```
   C:\Users\BAKARY JAMMEH\OneDrive - Università degli Studi di Milano-Bicocca\Desktop\MODELLING\Italian_cge_model\ipopt_solver\Ipopt-3.14.16-win64-msvs2019-md\bin
   ```
7. Click **"OK"** on all dialog boxes
8. **Restart your computer** or log off and back on

### Method 3: Command Line (Administrator)
1. Open **Command Prompt as Administrator**
2. Run:
   ```cmd
   setx PATH "%PATH%;C:\Users\BAKARY JAMMEH\OneDrive - Università degli Studi di Milano-Bicocca\Desktop\MODELLING\Italian_cge_model\ipopt_solver\Ipopt-3.14.16-win64-msvs2019-md\bin" /M
   ```

## Verification Steps
After any system-wide installation:

1. **Open a new PowerShell window** (not as administrator)
2. Run: `ipopt.exe --version`
3. If you see version info, it's working system-wide!

## What You Have Now ✅

### Current User Installation (Working)
- ✅ IPOPT available in PATH for your user account
- ✅ Works in new PowerShell sessions
- ✅ Works with Python/Pyomo
- ✅ No restart required
- ✅ Italian CGE model ready to run

### System-Wide Installation (Optional)
- ⚠️ Only needed if other users will use IPOPT
- ⚠️ Requires administrator privileges
- ⚠️ May require restart

## Your Italian CGE Model is Ready!

You can now:
1. **Open any new PowerShell session**
2. **Navigate to your model directory**
3. **Run your CGE model** with full IPOPT support
4. **All optimization problems** will work perfectly

The installation is **permanent** for your user account! 🎉