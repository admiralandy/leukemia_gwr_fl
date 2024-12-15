SELECT * FROM fl_county;
SELECT * FROM pesticides;

WITH intersected AS (
    SELECT
        c.county_fip,
        ST_Intersection(c.geom, p.geom) AS geom
    FROM
        fl_county c
    JOIN
        pesticides p
    ON
        ST_Intersects(c.geom, p.geom)
),
area_calculated AS (
    SELECT
        county_fip,
        ST_Area(geom::geography) AS pesticide_area
    FROM
        intersected
)
SELECT
    c.county_fip as FIPS,
    SUM(a.pesticide_area) AS total_pesticide_area,
    ST_Area(c.geom::geography) AS county_area,
    ROUND((SUM(a.pesticide_area) / ST_Area(c.geom::geography) * 100)::numeric,2) AS pesticide_pct
FROM
    fl_county c
LEFT JOIN
    area_calculated a
ON
    c.county_fip = a.county_fip
GROUP BY
    c.county_fip, c.geom
ORDER BY
    c.county_fip;
