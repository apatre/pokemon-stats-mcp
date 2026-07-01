SELECT
    id AS version_group_id,
    name AS version_group_name,
    json_extract_string(data, '$.generation.name') AS generation_name
FROM {{ source('staging', 'version_group') }}
