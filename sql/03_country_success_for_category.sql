SELECT
  country,
  COUNT(*) AS total,
  SUM(state='successful') AS success,
  ROUND(100 * SUM(state='successful')/COUNT(*), 2) AS success_rate
FROM projects
WHERE state IN ('successful','failed')
  AND main_category = %s      -- 由 visualize.py 傳入，例如 'Games'
GROUP BY country
HAVING COUNT(*) >= %s         -- 由 visualize.py 傳入，例如 50
ORDER BY success_rate DESC, country ASC;
