-- Ranks metal band origins by total number of fans.
-- Displays origin names and total fans, descending.

SELECT origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
