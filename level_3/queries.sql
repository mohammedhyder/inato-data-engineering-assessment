
-- Q1: Oncology specialization rate for each academic site
SELECT
    site_name,
    COUNT(*) AS total_applications,
    SUM(
        CASE
            WHEN LOWER(therapeutic_area) = 'oncology' THEN 1
            ELSE 0
        END
    ) AS oncology_applications,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN LOWER(therapeutic_area) = 'oncology' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS oncology_specialization_rate_pct
FROM application
WHERE LOWER(site_category) = 'academic'
GROUP BY site_name
ORDER BY oncology_specialization_rate_pct DESC;


-- Q2: Sites with at least 10 applications
-- in the 14-day window beginning with their first application
WITH first_applications AS (
    SELECT
        site_name,
        MIN(created_at) AS first_application_at
    FROM application
    GROUP BY site_name
)
SELECT
    a.site_name,
    f.first_application_at,
    COUNT(*) AS applications_in_14_days
FROM application AS a
JOIN first_applications AS f
    ON a.site_name = f.site_name
WHERE a.created_at >= f.first_application_at
  AND a.created_at < DATE_ADD(
      f.first_application_at,
      INTERVAL 14 DAY
  )
GROUP BY
    a.site_name,
    f.first_application_at
HAVING COUNT(*) >= 10
ORDER BY applications_in_14_days DESC;