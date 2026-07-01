SELECT
    id AS pokedex_id,
    name AS pokedex_name,
    CAST(json_extract_string(data, '$.is_main_series') AS BOOLEAN) AS is_main_series,
    CAST(regexp_extract(json_extract_string(data, '$.region.url'), 'region/([0-9]+)', 1) AS INTEGER) AS region_id,
    json_extract_string(data, '$.version_groups') AS version_group_names
FROM {{ source('staging', 'pokedex') }}
