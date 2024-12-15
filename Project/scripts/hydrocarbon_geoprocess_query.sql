SELECT * FROM fl_county;
SELECT * FROM fl_hydrocarbon;
ALTER TABLE fl_hydrocarbon
ADD COLUMN geom_2236 geometry(Multipolygon, 2236);
UPDATE fl_hydrocarbon
SET geom_2236 = ST_Transform(geom, 2236);
SELECT ST_SRID(geom) FROM fl_hydrocarbon;

SELECT 
  c.county_fip AS fips,
  c.name, 
  ROUND(
    (ST_Area(ST_Intersection(h.geom, c.geom)) / ST_Area(c.geom) * 100)::numeric, 
    2
  ) AS hydrocarbon_percentage
FROM fl_county c
JOIN fl_hydrocarbon h
  ON ST_Intersects(h.geom, c.geom)
ORDER BY hydrocarbon_percentage DESC;