-- Lists bands with Glam rock as main style, ranked by longevity.
-- Displays band names and lifespan (years).

SELECT band_name, (IFNULL(split, 2022) - formed) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
