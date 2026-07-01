WITH unnested AS (
    SELECT
        name AS version_group_name,
        json_extract_string(mlm.val, '$.name') AS move_learn_method
    FROM {{ source('staging', 'version_group') }},
    LATERAL unnest(json_transform(json_extract(data, '$.move_learn_methods'), '["JSON"]')) AS mlm(val)
)
SELECT
    md5(version_group_name || '_' || move_learn_method) AS sur_version_group_move_learn_method,
    version_group_name,
    move_learn_method
FROM unnested
