# Singapore Heat Stress Analysis

## Project Overview

This project analyzes heat stress across Singapore using open data from the National Environment Agency (NEA). I built an end-to-end ETL pipeline that:

- Extracts weather data (temperature, humidity, rainfall, wind speed) from data.gov.sg API
- Transforms and cleans the data using Python and Pandas
- Loads the data into a PostgreSQL database
- Analyzes which weather stations recorded the highest temperatures
- Visualizes results in Power BI

## Business Problem

Singapore's highly urbanized environment creates an urban heat island effect, where built-up areas experience higher temperatures than surrounding regions. This impacts:

- Public health (heat stress, heat-related illnesses)
- Energy consumption (increased air conditioning use)
- Urban livability (outdoor comfort, productivity)

**Key questions answered:**
- Which 10 weather stations recorded the highest daily average temperatures?
- Which 10 stations recorded the highest monthly average temperatures (Oct-Dec 2025)?

## Technology Stack

| Category | Tools |
|----------|-------|
| Programming | Python 3.x |
| Data Processing | Pandas, NumPy |
| API Integration | Requests, JSON |
| Database | PostgreSQL, SQLAlchemy |
| Visualization | Power BI |
| Environment | Jupyter Notebook |

## Architecture Diagram

      ================================================================================
                    SINGAPORE HEAT STRESS ANALYSIS - ETL PIPELINE
      ================================================================================

               ┌─────────────────────┐
               │    DATA SOURCE      │
               │  data.gov.sg API    │
               │  NEA Air Temp       │
               │  JSON via REST      │
               └──────────┬──────────┘
                          │
                          ▼
                ┌─────────────────────┐
                │     EXTRACT         │
                │  Python + requests  │
                │  For-loop: 92 days  │
                │  (Oct-Dec 2025)     │
                │  API key auth       │
                └──────────┬──────────┘
                           │
                           ▼
                 ┌─────────────────────┐
                 │    TRANSFORM        │
                 │  Python + Pandas    │
                 │  Flatten JSON       │
                 │  Clean missing      │
                 │  Remove duplicates  │
                 │  Validate temp      │
                 │  Add date/month/hr  │
                 └──────────┬──────────┘
                            │
                            ▼
                  ┌─────────────────────┐
                  │      LOAD           │
                  │  PostgreSQL         │
                  │  SQLAlchemy         │
                  │  Table: air_temp_df │
                  │  10+ columns        │
                  └──────────┬──────────┘
                             │
                             ▼
                   ┌─────────────────────┐
                   │  ANALYZE & VISUALIZE│
                   │  SQL Queries        │
                   │  Top 10 stations    │
                   │  Daily/monthly avg  │
                   └──────────┬──────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │  Power BI Dashboard │
                    │  Heat stress viz    │
                    └─────────────────────┘

      ================================================================================
                    FUTURE AUTOMATION (Planned)
      ================================================================================
                    ┌─────────────────────────┐
                    │  Apache Airflow          │
                    │  Daily scheduled ETL     │
                    │  Automatic data refresh  │
                    └─────────────────────────┘

## ETL Process

### 1. Extract
- Called data.gov.sg REST API using Python `requests` library
- Handled pagination across 92 days (Oct 1 - Dec 31, 2025)
- Used API key authentication to avoid rate limiting (HTTP 429 errors)

### 2. Transform
- Flattened nested JSON into tabular format
- Cleaned missing values
- Removed duplicate records
- Standardized data types (timestamp, float for temperature)
- Validated temperature ranges (23°C - 36°C for Singapore)

### 3. Load
- Created PostgreSQL database schema
- Used SQLAlchemy ORM to write DataFrame to database
- Implemented idempotent loading (append mode)

## Database Schema

```mermaid
erDiagram
    air_temp_df {
        SERIAL id PK
        TIMESTAMP timestamp
        VARCHAR(10) station_id
        VARCHAR(100) station_name
        REAL latitude
        REAL longitude
        REAL readings
        DATE date
        INTEGER month
        INTEGER hour
    }
    
    stations_master {
        VARCHAR(10) station_id PK
        VARCHAR(100) station_name
        REAL latitude
        REAL longitude
        VARCHAR(50) region
    }
    
    daily_aggregates {
        DATE date PK
        REAL avg_temp
        REAL max_temp
        REAL min_temp
        INTEGER total_readings
    }
    
    air_temp_df ||--o{ daily_aggregates : "aggregates by date"
    air_temp_df }o--|| stations_master : "references"
```

**Table Structure: air_temp_df**

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key (auto-generated) |
| timestamp | TIMESTAMP | Time of reading (SGT) |
| station_id | VARCHAR(4) | Unique station code |
| station_name | VARCHAR(100) | Station location name |
| latitude | REAL | Geographic latitude |
| longitude | REAL | Geographic longitude |
| readings | REAL | Temperature in Celsius |

### Planned Future Tables

| Table | Purpose |
|-------|---------|
| stations_master | Lookup table for station metadata |
| daily_aggregates | Pre-computed daily summaries |
| heat_stress_log | Historical heat stress calculations |

### Sample Query

```sql
-- Find the top 5 hottest stations in October 2025
SELECT 
    station_name,
    ROUND(AVG(readings), 1) as avg_temp
FROM air_temp_df
WHERE month = 10
GROUP BY station_name
ORDER BY avg_temp DESC
LIMIT 5;
```

## Key Findings

### Top 10 Hottest Locations (Oct-Dec 2025)

1. Paya Lebar
2. Pulau Ubin
3. Kim Chuan Road
4. Upper Changi
5. Clementi Road
6. Sentosa
7. Ang Mo Kio
8. Scotts Road
9. Banyan Road
10. Nanyang Avenue

### Weather Patterns Summary

| Metric | Observation |
|--------|-------------|
| Temperature | Consistently 28°C - 31°C, limited cooling periods |
| Humidity | 60% - 80%+, reduces evaporative cooling |
| Rainfall | Mostly 0mm, infrequent cooling events |
| Wind Speed | Below 6 knots, limited air circulation |

### Heat Stress Implications

The combination of high temperature + high humidity + low wind + infrequent rainfall creates conditions conducive to **cumulative heat stress**, even without extreme weather events.

## How to Run This Project

### Prerequisites

- Python 3.x
- PostgreSQL installed locally
- Power BI Desktop (for dashboard)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/singapore-heat-stress-analysis.git
cd singapore-heat-stress-analysis

# Install dependencies
pip install -r requirements.txt
```

