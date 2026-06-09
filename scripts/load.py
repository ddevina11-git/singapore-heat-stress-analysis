"""
Load: Write cleaned data to PostgreSQL database
Project: Singapore Heat Stress Analysis
"""

import pandas as pd
import sqlalchemy as db
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy import text
import os

# ============= CONFIGURATION =============
# Update these values with your PostgreSQL setup
USERNAME = 'postgres'
PASSWORD = os.getenv('POSTGRES_PASSWORD', 'your_password_here')
HOST = 'localhost'
PORT = 5432
DB_NAME = 'SGWeather'

CONNECTION_STRING = f'postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'

# ============= CREATE DATABASE IF NOT EXISTS =============
engine = db.create_engine(CONNECTION_STRING)

if not database_exists(engine.url):
    create_database(engine.url)
    print(f"Database '{DB_NAME}' created successfully!")
else:
    print(f"Database '{DB_NAME}' already exists")

# Dispose and reconnect
engine.dispose()
engine = db.create_engine(CONNECTION_STRING)
print(f"Connected to database: {DB_NAME}")

# ============= CREATE TABLE =============
create_table_sql = """
DROP TABLE IF EXISTS air_temp_df CASCADE;

CREATE TABLE air_temp_df (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    station_id VARCHAR(10),
    station_name VARCHAR(100),
    latitude REAL,
    longitude REAL,
    readings REAL,
    date DATE,
    month INTEGER,
    hour INTEGER
);
"""

with engine.begin() as conn:
    conn.execute(text(create_table_sql))
    print("Table 'air_temp_df' created successfully!")

# ============= LOAD DATA =============
# Load cleaned CSV
df = pd.read_csv('../data/processed/air_temp_cleaned.csv')
print(f"Loading {len(df)} rows into PostgreSQL...")

# Write to database
rows_written = df.to_sql(
    name='air_temp_df',
    con=engine,
    if_exists='append',
    index=False
)

print(f"Successfully loaded {rows_written} rows into 'air_temp_df' table")

# Verify load
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM air_temp_df"))
    count = result.scalar()
    print(f"Verification: {count} total rows in database")
