WITH unnested AS (
    SELECT
        name AS pokemon_name,
        CAST(json_extract_string(t.val, '$.slot') AS INTEGER) AS slot,
        json_extract_string(t.val, '$.type.name') AS type_name
    FROM {{ source('staging', 'pokemon') }},
    LATERAL unnest(json_transform(json_extract(data, '$.types'), '["JSON"]')) AS t(val)
)
SELECT
    md5(pokemon_name || '_' || slot) AS sur_pokemon_type_id,
    pokemon_name,
    slot,
    type_name
FROM unnested
