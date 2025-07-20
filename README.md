## Google Sheets to Snowflake Sync

This project automatically syncs a Google Sheet into a Snowflake table for use in tools like ThoughtSpot.

## Features
- Pulls latest data from a Google Sheet
- Uploads to Snowflake table (CREATE OR REPLACE)
- Runs on a schedule via Windows Task Scheduler

## Setup

### 1. Google Sheets
- Enable Sheets API on Google Cloud
- Download service account credentials
- Share your sheet with the service account email

### 2. Snowflake
- Create a user & role
- Grant write access to the target schema

### 3. Configuration
Update `config/config.yaml` with your values.

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Schedule via Windows
Create a Windows Task:
- Action: Start a program
- Program: `scripts/run_sync.bat`

## License
MIT
