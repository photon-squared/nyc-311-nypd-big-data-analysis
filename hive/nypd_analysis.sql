-- Crime counts by borough
SELECT 
  boro_nm, 
  COUNT(*) AS total_crimes
FROM tmp_nypd
GROUP BY boro_nm
ORDER BY total_crimes DESC;


-- Top 10 crime types
SELECT 
  ofns_desc, 
  COUNT(*) AS total
FROM tmp_nypd
GROUP BY ofns_desc
ORDER BY total DESC
LIMIT 10;


-- Top 10 high-crime precincts
SELECT 
  addr_pct_cd, 
  COUNT(*) AS total
FROM tmp_nypd
GROUP BY addr_pct_cd
ORDER BY total DESC
LIMIT 10;


-- Crime counts by month
SELECT 
  CAST(SUBSTR(cmplnt_fr_dt, 1, 2) AS INT) AS month,
  COUNT(*) AS total
FROM nypd_complaints
WHERE cmplnt_fr_dt LIKE '%2025'
GROUP BY CAST(SUBSTR(cmplnt_fr_dt, 1, 2) AS INT)
ORDER BY month;


-- Crime counts by borough and month
SELECT 
  boro_nm,
  CAST(SUBSTR(cmplnt_fr_dt, 1, 2) AS INT) AS month,
  COUNT(*) AS total
FROM nypd_2025_clean
WHERE boro_nm IS NOT NULL
GROUP BY boro_nm, CAST(SUBSTR(cmplnt_fr_dt, 1, 2) AS INT)
ORDER BY boro_nm, month;


-- Crime severity distribution
SELECT 
  law_cat_cd,
  COUNT(*) AS total,
  COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS proportion
FROM nypd_2025_clean
WHERE law_cat_cd IS NOT NULL
GROUP BY law_cat_cd;


-- Crime counts by suspect age group and severity
SELECT 
  susp_age_group,
  law_cat_cd,
  COUNT(*) AS total
FROM nypd_2025_clean
WHERE susp_age_group IN ('<18','18-24','25-44','45-64','65+')
  AND law_cat_cd IN ('FELONY','MISDEMEANOR','VIOLATION')
GROUP BY susp_age_group, law_cat_cd
ORDER BY susp_age_group, total DESC;


-- Crime counts by suspect gender and age group
SELECT 
  susp_sex,
  susp_age_group,
  COUNT(*) AS total
FROM nypd_2025_clean
WHERE susp_sex IN ('M','F')
  AND susp_age_group IN ('<18','18-24','25-44','45-64','65+')
GROUP BY susp_sex, susp_age_group
ORDER BY total DESC;


-- Crime counts by suspect race / ethnic group
SELECT 
  susp_race,
  COUNT(*) AS total,
  COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS proportion
FROM nypd_2025_clean
WHERE susp_race IS NOT NULL
  AND susp_race != 'UNKNOWN'
GROUP BY susp_race
ORDER BY total DESC;


-- Victim profile distribution
SELECT 
  a.vic_sex,
  a.total,
  a.total / b.total_sum AS proportion
FROM (
    SELECT 
      vic_sex,
      COUNT(*) AS total
    FROM nypd_2025_clean
    WHERE vic_sex IS NOT NULL
    GROUP BY vic_sex
) a
JOIN (
    SELECT 
      COUNT(*) AS total_sum
    FROM nypd_2025_clean
    WHERE vic_sex IS NOT NULL
) b
ORDER BY a.total DESC;
