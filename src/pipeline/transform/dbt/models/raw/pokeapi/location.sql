WITH unnested AS (
    SELECT
        id AS location_id,
        name AS location_name,
        json_extract_string(data, '$.region.name') AS region_name,
        json_extract_string(area.val, '$.name') AS location_area_name
    FROM {{ source('staging', 'location') }},
    LATERAL unnest(json_transform(json_extract(data, '$.areas'), '["JSON"]')) AS area(val)
)
SELECT
    md5(location_id || '_' || location_area_name) AS sur_location_area_name,
    location_id,
    location_name,
    region_name,
    location_area_name
FROM unnested
