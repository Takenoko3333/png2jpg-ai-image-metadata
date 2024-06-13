@echo off
@REM Change directory to the location of the Python script
cd /d %~dp0

echo Converting PNG files to JPEG...

python png2jpg.py

echo Conversion completed.

@REM If you want to keep the command line open after processing, uncomment @REM pause.
@REM pause
