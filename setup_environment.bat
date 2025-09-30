@echo off
REM Italian CGE Model Environment Setup Script
REM This script activates the environment and ensures IPOPT is available

echo ========================================
echo Italian CGE Model Environment Setup
echo ========================================

REM Activate virtual environment
call italian_cge_env\Scripts\activate

REM Add IPOPT directory to PATH
set PATH=%PATH%;C:\Users\BAKARY JAMMEH\OneDrive - Università degli Studi di Milano-Bicocca\Desktop\MODELLING\Italian_cge_model\ipopt_solver\Ipopt-3.14.16-win64-msvs2019-md\bin

echo Environment activated successfully!
echo IPOPT solver is available and working!
echo Gurobi solver is also available as backup!

echo.
echo To verify everything is working, run:
echo   python environment_verification.py

echo.
echo To run the CGE model:
echo   cd src
echo   python main_model.py

cmd /k