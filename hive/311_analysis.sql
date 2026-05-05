-- 311 monthly complaint counts by borough
SELECT 
  borough,
  SUBSTR(created_date, 6, 2) AS month,
  COUNT(*) AS total
FROM nyc_311
WHERE borough IS NOT NULL
  AND created_date IS NOT NULL
GROUP BY borough, SUBSTR(created_date, 6, 2)
ORDER BY borough, month;


-- 311 complaint counts by borough
SELECT 
  borough,
  COUNT(*) AS total
FROM nyc_311
WHERE borough IS NOT NULL
GROUP BY borough
ORDER BY total DESC;


-- 311 complaint counts by police precinct
SELECT 
  police_precinct,
  COUNT(*) AS total
FROM nyc_311
WHERE police_precinct IS NOT NULL
GROUP BY police_precinct
ORDER BY total DESC;


-- 311 complaint counts by complaint type
SELECT 
  complaint_type,
  COUNT(*) AS total
FROM nyc_311
WHERE complaint_type IS NOT NULL
GROUP BY complaint_type
ORDER BY total DESC;


-- 311 monthly complaint counts
SELECT 
  SUBSTR(created_date, 6, 2) AS month,
  COUNT(*) AS total
FROM nyc_311
WHERE created_date IS NOT NULL
GROUP BY SUBSTR(created_date, 6, 2)
ORDER BY month;


-- 311 complaint counts by agency / department
SELECT 
  agency_name,
  COUNT(*) AS total
FROM nyc_311
WHERE agency_name IS NOT NULL
GROUP BY agency_name
ORDER BY total DESC;
