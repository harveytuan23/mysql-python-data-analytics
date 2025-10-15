-- 各類別成功率
SELECT
  main_category,
  COUNT(*) AS total,
  SUM(state='successful') AS success,
  ROUND(100 * SUM(state='successful') / COUNT(*), 2) AS success_rate
FROM projects
WHERE state IN ('successful','failed')
GROUP BY main_category
ORDER BY success_rate DESC;