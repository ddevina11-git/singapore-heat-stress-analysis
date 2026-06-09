"""
Transform: Clean and validate extracted weather data
Project: Singapore Heat Stress Analysis
"""

import pandas as pd
import json

# Load raw data
with open('../data/raw/air_temp_raw.json', 'r') as f:
    raw_data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(raw_data)

print(f"Original shape: {df.shape}")
print(f"Original columns: {df.columns.tolist()}")

# ============= Data Cleaning Steps =============

# 1. Remove duplicates
initial_count = len(df)
df = df.drop_duplicates()
print(f"Removed {initial_count - len(df)} duplicate rows")

# 2. Handle missing values
missing_before = df.isnull().sum().sum()
df = df.dropna(subset=['temperature_c', 'station_id', 'timestamp'])
missing_after = df.isnull().sum().sum()
print(f"Removed {missing_before - missing_after} rows with missing critical values")

# 3. Standardize timestamp format
df['timestamp'] = pd.to_datetime(df['timestamp'])
print(f"Timestamp range: {df['timestamp'].min()} to {df['timestamp'].max()}")

# 4. Validate temperature ranges (Singapore typical range: 23°C - 36°C)
invalid_temps = df[(df['temperature_c'] < 23) | (df['temperature_c'] > 36)]
print(f"Found {len(invalid_temps)} records outside typical temperature range (23-36°C)")

# Remove invalid temperatures
df = df[(df['temperature_c'] >= 23) & (df['temperature_c'] <= 36)]
print(f"Shape after temperature validation: {df.shape}")

# 5. Add derived columns
df['date'] = df['timestamp'].dt.date
df['month'] = df['timestamp'].dt.month
df['hour'] = df['timestamp'].dt.hour

# 6. Rename column for database compatibility
df = df.rename(columns={'temperature_c': 'readings'})

print(f"\nFinal shape after cleaning: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# Save cleaned data to CSV
df.to_csv('../data/processed/air_temp_cleaned.csv', index=False)
print("\nCleaned data saved to data/processed/air_temp_cleaned.csv")

# Display sample
print("\nSample of cleaned data:")
print(df.head())
