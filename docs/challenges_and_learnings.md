# Challenges & Learnings

## Challenge 1: API Date Range Limitation

**Problem:** The data.gov.sg API only returns data for a single requested day. We needed 92 days of data (Oct-Dec 2025).

**Solution:** Implemented a Python for-loop that iterates through each date, constructs a new URL with the date parameter, and appends results to a list.

**Learning:** APIs often have built-in limitations. When designing pipelines, always check API documentation for pagination and date range capabilities.

## Challenge 2: Rate Limiting (HTTP 429 Errors)

**Problem:** After multiple API calls, we started receiving HTTP 429 (Too Many Requests) errors. The loop would fail mid-execution.

**Solution:** Registered for a free API key at data.gov.sg and added it to request headers. This increased our rate limits significantly.

**Learning:** Always check if an API requires authentication. Even "open" APIs often have higher limits for authenticated requests.

## Challenge 3: Missing Data for Some Timestamps

**Problem:** Some timestamps had no temperature readings from the API, even though NEA's website showed data existed.

**Solution:** Documented as a limitation. For the project scope, we worked with available data. Ideally, we would investigate the discrepancy and potentially merge from multiple endpoints.

**Learning:** Real-world data is never perfect. Documenting limitations is as important as showing results.

## Challenge 4: Inconsistent Station IDs Across Datasets

**Problem:** Air temperature, humidity, rainfall, and wind speed datasets had different numbers of stations and inconsistent station IDs.

**Solution:** Used air temperature as the primary table for analysis. For future iterations, we would create a station master lookup table to map IDs across datasets.

**Learning:** Data integration across multiple sources requires careful planning of primary keys and foreign key relationships.
