SELECT
    id AS version_id,
    name AS version_name,
    CAST(regexp_extract(json_extract_string(data, '$.version_group.url'), 'version-group/([0-9]+)', 1) AS INTEGER) AS version_group_id
FROM {{ source('staging', 'version') }}
