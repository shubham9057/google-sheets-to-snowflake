import pandas as pd
import gspread
import snowflake.connector
import yaml
import os
from oauth2client.service_account import ServiceAccountCredentials

# Load config
with open(os.path.join(".", "config", "config.yaml")) as f:
    config = yaml.safe_load(f)

# Load Snowflake credentials
with open(os.path.join(".", "credentials", "snowflake_credentials.yaml")) as f:
    creds = yaml.safe_load(f)

# Merge both into config
config["snowflake"].update(creds["snowflake"])

# Google Auth
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(".", "credentials", "credentials.json"), scopes)
client = gspread.authorize(creds)

# Read Google Sheet
sheet_id = config["google_sheet"]["sheet_id"]
worksheet_name = config["google_sheet"]["worksheet_name"]

worksheet = client.open_by_key(sheet_id).worksheet(worksheet_name)
records = worksheet.get_all_records()
df = pd.DataFrame(records)

# Snowflake connection
sf = config["snowflake"]
conn = snowflake.connector.connect(
    account = sf["account"],
    user = sf["user"],
    authenticator = 'SNOWFLAKE_JWT',
    private_key_file = sf["private_key_file"],
    private_key_file_pwd = sf["private_key_file_pwd"],
    warehouse = sf["warehouse"],
    database = sf["database"],
    schema = sf["schema"],
    role = sf["role"]
)

cs = conn.cursor()

# Create or replace table
columns = ', '.join([f'"{col}" STRING' for col in df.columns])
table_name = f'{sf["database"]}.{sf["schema"]}.{sf["table_name"]}'
cs.execute(f'CREATE OR REPLACE TABLE {table_name} ({columns})')

# Upload data
for _, row in df.iterrows():
    values = tuple(str(val) if val is not None else None for val in row)
    placeholders = ', '.join(['%s'] * len(values))
    insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
    cs.execute(insert_query, values)

cs.close()
conn.close()

print("✅ Sync complete.")