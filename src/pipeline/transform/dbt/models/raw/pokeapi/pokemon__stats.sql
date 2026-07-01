WITH unnested AS (
    SELECT
        name AS pokemon_name,
        json_extract_string(stat.val, '$.stat.name') AS stat_name,
        CAST(json_extract_string(stat.val, '$.base_stat') AS INTEGER) AS base_stat,
        CAST(json_extract_string(stat.val, '$.effort') AS INTEGER) AS effort
    FROM {{ source('staging', 'pokemon') }},
    LATERAL unnest(json_transform(json_extract(data, '$.stats'), '["JSON"]')) AS stat(val)
)
SELECT
    md5(pokemon_name || '_' || stat_name) AS sur_pokemon_stats_id,
    pokemon_name,
    stat_name,
    base_stat,
    effort
FROM unnested
