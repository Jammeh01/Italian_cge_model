@echo off
REM Italian CGE Model Environment Setup Script
REM This script activates the environment and ensures IPOPT is available

echo ========================================
echo Italian CGE Model Environment Setup
echo ========================================

REM Activate virtual environment
call italian_cge_env\Scripts\activate

REM Add IDAES bin directory to PATH for IPOPT
set PATH=%PATH%;C:\Users\BAKARY JAMMEH\AppData\Local\idaes\bin

echo Environment activated successfully!
echo IPOPT solver is available at: C:\Users\BAKARY JAMMEH\AppData\Local\idaes\bin\ipopt.exe

echo.
echo To verify everything is working, run:
echo   python environment_verification.py

echo.
echo To run the CGE model:
echo   cd src
echo   python main_model.py

cmd /k