WITH base_types AS (
    SELECT
        name AS type_name,
        json_extract(data, '$.damage_relations') AS dr
    FROM {{ source('staging', 'type') }}
),
double_from AS (
    SELECT
        type_name AS target_type,
        json_extract_string(t.val, '$.name') AS damage_type,
        2.0 AS damage_factor
    FROM base_types,
    LATERAL unnest(json_transform(json_extract(dr, '$.double_damage_from'), '["JSON"]')) AS t(val)
),
double_to AS (
    SELECT
        json_extract_string(t.val, '$.name') AS target_type,
        type_name AS damage_type,
        2.0 AS damage_factor
    FROM base_types,
    LATERAL unnest(json_transform(json_extract(dr, '$.double_damage_to'), '["JSON"]')) AS t(val)
),
half_from AS (
    SELECT
        type_name AS target_type,
        json_extract_string(t.val, '$.name') AS damage_type,
        0.5 AS damage_factor
    FROM base_types,
    LATERAL unnest(json_transform(json_extract(dr, '$.half_damage_from'), '["JSON"]')) AS t(val)
),
half_to AS (
    SELECT
        json_extract_string(t.val, '$.name') AS target_type,
        type_name AS damage_type,
        0.5 AS damage_factor
    FROM base_types,
    LATERAL unnest(json_transform(json_extract(dr, '$.half_damage_to'), '["JSON"]')) AS t(val)
),
no_from AS (
    SELECT
        type_name AS target_type,
        json_extract_string(t.val, '$.name') AS damage_type,
        0.0 AS damage_factor
    FROM base_types,
    LATERAL unnest(json_transform(json_extract(dr, '$.no_damage_from'), '["JSON"]')) AS t(val)
),
no_to AS (
    SELECT
        json_extract_string(t.val, '$.name') AS target_type,
        type_name AS damage_type,
        0.0 AS damage_factor
    FROM base_types,
    LATERAL unnest(json_transform(json_extract(dr, '$.no_damage_to'), '["JSON"]')) AS t(val)
),
combined AS (
    SELECT * FROM double_from
    UNION ALL
    SELECT * FROM double_to
    UNION ALL
    SELECT * FROM half_from
    UNION ALL
    SELECT * FROM half_to
    UNION ALL
    SELECT * FROM no_from
    UNION ALL
    SELECT * FROM no_to
)
SELECT DISTINCT
    md5(damage_type || '_' || target_type || '_' || damage_factor) AS sur_type_relation_id,
    damage_type,
    target_type,
    damage_factor
FROM combined
