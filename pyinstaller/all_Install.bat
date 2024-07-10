@echo off
setlocal

rem Function to find the latest Maya path
set "base_path=C:\Program Files\Autodesk"
if not exist "%base_path%" (
    echo Cannot find Autodesk directory at %base_path%
    goto end
)

rem Find all Maya directories
for /d %%d in ("%base_path%\Maya*") do (
    set "maya_dirs=!maya_dirs! %%d"
)

if not defined maya_dirs (
    echo Cannot find any Maya installation in the Autodesk directory.
    goto end
)

rem Sort and select the latest Maya directory
for %%d in (%maya_dirs%) do (
    set "latest_maya_dir=%%d"
)

set "mayapy_path=%latest_maya_dir%\bin\mayapy.exe"

if not exist "%mayapy_path%" (
    echo Cannot find mayapy.exe at %mayapy_path%
    goto end
)

rem Get the current directory
set "current_dir=%~dp0"
set "script_to_run=%current_dir%all_Install.py"

rem Run the script with mayapy
"%mayapy_path%" "%script_to_run%"

:end
endlocal
pause
