@echo off

REM Change directory to project path
cd /d C:\Users\Atrium\Documents\ThoughtSpot\google-sheet-to-snowflake

REM Activate the virtual environment
call venv\Scripts\activate

REM Run the sync script
call python ./scripts/sync_google_sheet.py