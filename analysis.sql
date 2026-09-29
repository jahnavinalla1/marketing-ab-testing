-- name: variants
SELECT variant,COUNT(*) users,SUM(converted) conversions,
 ROUND(100.0*SUM(converted)/COUNT(*),3) conversion_pct,
 ROUND(SUM(revenue_cents)/100.0,2) revenue,
 ROUND(AVG(revenue_cents)/100.0,4) revenue_per_user,
 ROUND(SUM(acquisition_cents)/100.0,2) acquisition_cost
FROM experiment GROUP BY variant ORDER BY variant;
-- name: device_diagnostics
SELECT device,variant,COUNT(*) users,SUM(converted) conversions,
 ROUND(100.0*AVG(converted),3) conversion_pct
FROM experiment GROUP BY device,variant ORDER BY device,variant;
