WITH unnested AS (
    SELECT
        id AS pokemon_species_id,
        CAST(regexp_extract(json_extract_string(var.val, '$.pokemon.url'), 'pokemon/([0-9]+)', 1) AS INTEGER) AS pokemon_id
    FROM {{ source('staging', 'pokemon_species') }},
    LATERAL unnest(json_transform(json_extract(data, '$.varieties'), '["JSON"]')) AS var(val)
)
SELECT
    md5(pokemon_species_id || '_' || pokemon_id) AS sur_pokemon_species_id_pokemon_id,
    pokemon_species_id,
    pokemon_id
FROM unnested
