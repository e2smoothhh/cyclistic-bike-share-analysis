-- ============================================================
-- Cyclistic Bike-Share Case Study
-- Phase 4: Analyze — SQL Queries (BigQuery / PostgreSQL)
-- Run these after uploading cyclistic_clean.csv to your DB
-- ============================================================


-- ── SETUP: Create the main table (BigQuery syntax) ────────────
-- If using PostgreSQL, replace backticks with double-quotes
-- and adjust TIMESTAMP parsing as needed.

/*
CREATE TABLE cyclistic.trips AS
SELECT * FROM cyclistic.cyclistic_clean;
*/


-- ── Q1: Total rides and share by rider type ───────────────────
SELECT
  member_casual                                        AS rider_type,
  COUNT(*)                                             AS total_rides,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1)  AS pct_of_total
FROM cyclistic.trips
GROUP BY member_casual
ORDER BY total_rides DESC;


-- ── Q2: Average, median, and max ride length by rider type ────
SELECT
  member_casual                            AS rider_type,
  ROUND(AVG(ride_length_min), 2)           AS avg_ride_min,
  ROUND(APPROX_QUANTILES(ride_length_min, 2)[OFFSET(1)], 2) AS median_ride_min,
  ROUND(MAX(ride_length_min), 2)           AS max_ride_min,
  COUNT(*)                                 AS total_rides
FROM cyclistic.trips
GROUP BY member_casual;


-- ── Q3: Ride count and avg duration by day of week ────────────
SELECT
  member_casual       AS rider_type,
  day_name,
  day_of_week,
  COUNT(*)            AS ride_count,
  ROUND(AVG(ride_length_min), 2) AS avg_ride_min
FROM cyclistic.trips
GROUP BY member_casual, day_name, day_of_week
ORDER BY member_casual, day_of_week;


-- ── Q4: Monthly ride volume (seasonality) ─────────────────────
SELECT
  member_casual  AS rider_type,
  year,
  month,
  month_name,
  season,
  COUNT(*)       AS ride_count,
  ROUND(AVG(ride_length_min), 2) AS avg_ride_min
FROM cyclistic.trips
GROUP BY member_casual, year, month, month_name, season
ORDER BY year, month, member_casual;


-- ── Q5: Bike type preferences by rider type ───────────────────
SELECT
  member_casual  AS rider_type,
  rideable_type  AS bike_type,
  COUNT(*)       AS ride_count,
  ROUND(COUNT(*) * 100.0 /
    SUM(COUNT(*)) OVER (PARTITION BY member_casual), 1) AS pct_within_type
FROM cyclistic.trips
GROUP BY member_casual, rideable_type
ORDER BY member_casual, ride_count DESC;


-- ── Q6: Hourly usage pattern ──────────────────────────────────
SELECT
  member_casual  AS rider_type,
  hour,
  COUNT(*)       AS ride_count
FROM cyclistic.trips
GROUP BY member_casual, hour
ORDER BY member_casual, hour;


-- ── Q7: Peak hours for casual vs member riders ────────────────
WITH hourly AS (
  SELECT
    member_casual,
    hour,
    COUNT(*) AS ride_count,
    RANK() OVER (PARTITION BY member_casual ORDER BY COUNT(*) DESC) AS rnk
  FROM cyclistic.trips
  GROUP BY member_casual, hour
)
SELECT member_casual AS rider_type, hour, ride_count
FROM hourly
WHERE rnk <= 5
ORDER BY member_casual, rnk;


-- ── Q8: Top 15 start stations for casual riders ───────────────
SELECT
  start_station_name  AS station,
  COUNT(*)            AS casual_rides
FROM cyclistic.trips
WHERE member_casual = 'casual'
  AND start_station_name IS NOT NULL
GROUP BY start_station_name
ORDER BY casual_rides DESC
LIMIT 15;


-- ── Q9: Weekend vs weekday split ──────────────────────────────
SELECT
  member_casual AS rider_type,
  CASE
    WHEN day_of_week IN (1, 7) THEN 'Weekend'
    ELSE 'Weekday'
  END AS day_type,
  COUNT(*) AS ride_count,
  ROUND(AVG(ride_length_min), 2) AS avg_ride_min
FROM cyclistic.trips
GROUP BY member_casual, day_type
ORDER BY member_casual, day_type;


-- ── Q10: Season-level summary ─────────────────────────────────
SELECT
  member_casual AS rider_type,
  season,
  COUNT(*)      AS ride_count,
  ROUND(AVG(ride_length_min), 2) AS avg_ride_min
FROM cyclistic.trips
GROUP BY member_casual, season
ORDER BY member_casual,
  CASE season
    WHEN 'Spring' THEN 1
    WHEN 'Summer' THEN 2
    WHEN 'Fall'   THEN 3
    WHEN 'Winter' THEN 4
  END;
