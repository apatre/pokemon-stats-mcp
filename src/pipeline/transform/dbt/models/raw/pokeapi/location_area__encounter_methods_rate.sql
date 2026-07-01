WITH unnested_methods AS (
    SELECT
        id AS location_area_id,
        name AS location_area_name,
        json_extract_string(emr.val, '$.encounter_method.name') AS encounter_method,
        json_extract(emr.val, '$.version_details') AS version_details
    FROM {{ source('staging', 'location_area') }},
    LATERAL unnest(json_transform(json_extract(data, '$.encounter_method_rates'), '["JSON"]')) AS emr(val)
),
flat_details AS (
    SELECT
        location_area_id,
        location_area_name,
        encounter_method,
        json_extract_string(vd.val, '$.version.name') AS version_name,
        CAST(json_extract_string(vd.val, '$.rate') AS INTEGER) AS encounter_rate
    FROM unnested_methods,
    LATERAL unnest(json_transform(version_details, '["JSON"]')) AS vd(val)
)
SELECT
    md5(location_area_id || '_' || encounter_method || '_' || version_name) AS sur_location_area_encounter_method_rate,
    location_area_id,
    location_area_name,
    encounter_method,
    version_name,
    encounter_rate
FROM flat_details
