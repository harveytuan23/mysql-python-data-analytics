SELECT
  YEAR(launched) AS yr,
  COUNT(*) AS total,
  SUM(state='successful') AS success,
  ROUND(100 * SUM(state='successful')/COUNT(*), 2) AS success_rate
FROM projects
WHERE launched IS NOT NULL
  AND state IN ('successful','failed')
GROUP BY YEAR(launched)
HAVING yr IS NOT NULL
ORDER BY yr;
