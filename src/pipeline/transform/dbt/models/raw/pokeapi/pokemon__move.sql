WITH unnested_moves AS (
    SELECT
        name AS pokemon_name,
        json_extract_string(m.val, '$.move.name') AS move_name,
        json_extract(m.val, '$.version_group_details') AS details
    FROM {{ source('staging', 'pokemon') }},
    LATERAL unnest(json_transform(json_extract(data, '$.moves'), '["JSON"]')) AS m(val)
),
flat_details AS (
    SELECT
        pokemon_name,
        move_name,
        json_extract_string(vd.val, '$.version_group.name') AS version_group_name,
        json_extract_string(vd.val, '$.move_learn_method.name') AS move_learn_method,
        CAST(json_extract_string(vd.val, '$.level_learned_at') AS INTEGER) AS level_learned_at
    FROM unnested_moves,
    LATERAL unnest(json_transform(details, '["JSON"]')) AS vd(val)
)
SELECT
    md5(pokemon_name || '_' || move_name || '_' || version_group_name || '_' || move_learn_method || '_' || level_learned_at) AS sur_pokemon_move_id,
    pokemon_name,
    move_name,
    version_group_name,
    move_learn_method,
    level_learned_at
FROM flat_details
