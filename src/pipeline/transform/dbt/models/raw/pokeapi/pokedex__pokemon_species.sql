WITH unnested AS (
    SELECT
        name AS pokedex_name,
        CAST(json_extract_string(entry.val, '$.entry_number') AS INTEGER) AS pokemon_species_entry_id,
        json_extract_string(entry.val, '$.pokemon_species.name') AS pokemon_species_name
    FROM {{ source('staging', 'pokedex') }},
    LATERAL unnest(json_transform(json_extract(data, '$.pokemon_entries'), '["JSON"]')) AS entry(val)
)
SELECT
    md5(pokedex_name || '_' || pokemon_species_name) AS sur_pokedex_pokemon_species,
    pokedex_name,
    pokemon_species_entry_id,
    pokemon_species_name
FROM unnested
