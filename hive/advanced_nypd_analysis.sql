-- Crime counts by hour
SELECT 
  SUBSTR(cmplnt_fr_tm, 1, 2) AS hour,
  COUNT(*) AS total
FROM nypd_complaints
GROUP BY SUBSTR(cmplnt_fr_tm, 1, 2)
ORDER BY COUNT(*) DESC;


-- Felony crime counts by hour
SELECT 
  SUBSTR(cmplnt_fr_tm, 1, 2) AS hour,
  COUNT(*) AS total
FROM nypd_complaints
WHERE law_cat_cd = 'FELONY'
GROUP BY SUBSTR(cmplnt_fr_tm, 1, 2)
ORDER BY total DESC;


-- Most frequent crime type for each hour
SELECT 
  t1.hour,
  t1.ofns_desc,
  t1.total
FROM (
    SELECT 
        CAST(SUBSTR(cmplnt_fr_tm, 1, 2) AS INT) AS hour,
        ofns_desc,
        COUNT(*) AS total
    FROM nypd_2025_clean
    WHERE cmplnt_fr_tm IS NOT NULL
      AND ofns_desc IS NOT NULL
    GROUP BY CAST(SUBSTR(cmplnt_fr_tm, 1, 2) AS INT), ofns_desc
) t1
JOIN (
    SELECT 
        hour,
        MAX(cnt) AS max_cnt
    FROM (
        SELECT 
            CAST(SUBSTR(cmplnt_fr_tm, 1, 2) AS INT) AS hour,
            ofns_desc,
            COUNT(*) AS cnt
        FROM nypd_2025_clean
        GROUP BY CAST(SUBSTR(cmplnt_fr_tm, 1, 2) AS INT), ofns_desc
    ) t2
    GROUP BY hour
) t2
ON t1.hour = t2.hour
AND t1.total = t2.max_cnt
ORDER BY t1.hour;


-- Suspect gender/age and victim gender/age combined analysis
SELECT 
  susp_sex,
  susp_age_group,
  vic_sex,
  vic_age_group,
  COUNT(*) AS total
FROM nypd_2025_clean
WHERE susp_sex IS NOT NULL
  AND vic_sex IS NOT NULL
  AND susp_age_group IN ('<18','18-24','25-44','45-64','65+')
  AND vic_age_group IN ('<18','18-24','25-44','45-64','65+')
GROUP BY susp_sex, susp_age_group, vic_sex, vic_age_group
ORDER BY total DESC
LIMIT 20;


-- Suspect/victim demographic combination with crime type
SELECT 
  susp_sex,
  susp_age_group,
  vic_sex,
  vic_age_group,
  ofns_desc,
  COUNT(*) AS total
FROM nypd_2025_clean
WHERE susp_sex IN ('M','F')
  AND vic_sex IN ('M','F')
  AND susp_age_group IN ('<18','18-24','25-44','45-64','65+')
  AND vic_age_group IN ('<18','18-24','25-44','45-64','65+')
  AND ofns_desc IS NOT NULL
GROUP BY susp_sex, susp_age_group, vic_sex, vic_age_group, ofns_desc
ORDER BY total DESC
LIMIT 20;
