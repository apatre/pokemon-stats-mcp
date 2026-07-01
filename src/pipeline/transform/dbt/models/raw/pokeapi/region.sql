SELECT
    id AS region_id,
    name AS region_name,
    json_extract_string(data, '$.main_generation.name') AS main_generation
FROM {{ source('staging', 'region') }}
