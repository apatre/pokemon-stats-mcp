WITH unnested AS (
    SELECT
        name AS version_group_name,
        json_extract_string(reg.val, '$.name') AS region_name
    FROM {{ source('staging', 'version_group') }},
    LATERAL unnest(json_transform(json_extract(data, '$.regions'), '["JSON"]')) AS reg(val)
)
SELECT
    md5(version_group_name || '_' || region_name) AS sur_version_group_region_name,
    version_group_name,
    region_name
FROM unnested
