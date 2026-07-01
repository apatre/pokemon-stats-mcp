SELECT
    id AS pokemon_species_id,
    name AS pokemon_species_name,
    CAST(json_extract_string(data, '$.order') AS INTEGER) AS species_order,
    CAST(json_extract_string(data, '$.gender_rate') AS INTEGER) AS gender_rate,
    CAST(json_extract_string(data, '$.capture_rate') AS INTEGER) AS capture_rate,
    CAST(json_extract_string(data, '$.base_happiness') AS INTEGER) AS base_happiness,
    CAST(json_extract_string(data, '$.is_baby') AS BOOLEAN) AS is_baby,
    CAST(json_extract_string(data, '$.is_legendary') AS BOOLEAN) AS is_legendary,
    CAST(json_extract_string(data, '$.is_mythical') AS BOOLEAN) AS is_mythical,
    CAST(json_extract_string(data, '$.hatch_counter') AS INTEGER) AS hatch_counter,
    CAST(json_extract_string(data, '$.has_gender_differences') AS BOOLEAN) AS has_gender_differences,
    CAST(json_extract_string(data, '$.forms_switchable') AS BOOLEAN) AS forms_switchable,
    json_extract_string(data, '$.growth_rate.name') AS growth_rate,
    json_extract_string(data, '$.evolves_from_species.name') AS evolves_from_species,
    CAST(regexp_extract(json_extract_string(data, '$.evolution_chain.url'), 'evolution-chain/([0-9]+)', 1) AS INTEGER) AS evolution_chain_id,
    json_extract_string(data, '$.generation.name') AS generation_name
FROM {{ source('staging', 'pokemon_species') }}
