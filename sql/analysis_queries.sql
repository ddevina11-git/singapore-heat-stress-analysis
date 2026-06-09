-- ============================================
-- Singapore Heat Stress Analysis
-- SQL Queries for Analysis
-- ============================================

-- 1. Top 10 stations by daily average temperature
SELECT 
    station_name,
    DATE(timestamp) as date,
    AVG(readings) as avg_temp
FROM air_temp_df
GROUP BY station_name, DATE(timestamp)
ORDER BY avg_temp DESC
LIMIT 10;

-- 2. Top 10 stations by monthly average temperature (October 2025)
SELECT 
    station_name,
    AVG(readings) as avg_temp_oct
FROM air_temp_df
WHERE EXTRACT(MONTH FROM timestamp) = 10
GROUP BY station_name
ORDER BY avg_temp_oct DESC
LIMIT 10;

-- 3. Top 10 stations by monthly average temperature (November 2025)
SELECT 
    station_name,
    AVG(readings) as avg_temp_nov
FROM air_temp_df
WHERE EXTRACT(MONTH FROM timestamp) = 11
GROUP BY station_name
ORDER BY avg_temp_nov DESC
LIMIT 10;

-- 4. Top 10 stations by monthly average temperature (December 2025)
SELECT 
    station_name,
    AVG(readings) as avg_temp_dec
FROM air_temp_df
WHERE EXTRACT(MONTH FROM timestamp) = 12
GROUP BY station_name
ORDER BY avg_temp_dec DESC
LIMIT 10;

-- 5. Daily temperature summary statistics
SELECT 
    DATE(timestamp) as date,
    MIN(readings) as min_temp,
    MAX(readings) as max_temp,
    AVG(readings) as avg_temp,
    STDDEV(readings) as temp_stddev
FROM air_temp_df
GROUP BY DATE(timestamp)
ORDER BY date;

-- 6. Hourly temperature patterns (heat by time of day)
SELECT 
    hour,
    AVG(readings) as avg_temp,
    MIN(readings) as min_temp,
    MAX(readings) as max_temp
FROM air_temp_df
GROUP BY hour
ORDER BY hour;

-- 7. Stations with highest temperature variability
SELECT 
    station_name,
    AVG(readings) as avg_temp,
    MAX(readings) - MIN(readings) as temp_range,
    COUNT(*) as reading_count
FROM air_temp_df
GROUP BY station_name
HAVING COUNT(*) > 100
ORDER BY temp_range DESC
LIMIT 10;
