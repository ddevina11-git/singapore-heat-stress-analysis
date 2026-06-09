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

```mermaid
flowchart TB
    subgraph Source["1. Data Source"]
        A[("data.gov.sg API<br/>NEA Air Temperature")]
    end

    subgraph Extract["2. Extract (Python)"]
        B["requests + for-loop<br/>92 days (Oct-Dec 2025)<br/>API key authentication"]
    end

    subgraph Transform["3. Transform (Pandas)"]
        C["Flatten JSON → DataFrame<br/>Clean missing values<br/>Remove duplicates<br/>Validate temperature range<br/>Add date/month/hour columns"]
    end

    subgraph Load["4. Load (SQLAlchemy)"]
        D[("PostgreSQL Database<br/>'SGWeather'") ]
        E["Table: air_temp_df<br/>id, timestamp, station_id<br/>station_name, latitude<br/>longitude, readings<br/>date, month, hour"]
    end

    subgraph Analyze["5. Analyze & Visualize"]
        F["SQL Analysis Queries<br/>Top 10 stations<br/>Daily/monthly averages"]
        G["Power BI Dashboard<br/>Heat stress visualization"]
    end

    A --> B --> C --> D
    D --> E
    E --> F --> G

    subgraph Automation["Future: Automation"]
        H["Apache Airflow<br/>Daily scheduled pipeline"]
    end

    D -.-> H
```

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

# Install dependencies
pip install -r requirements.txt
