SELECT
    id AS pokemon_id,
    name AS pokemon_name,
    CAST(json_extract_string(data, '$.base_experience') AS INTEGER) AS base_experience,
    CAST(json_extract_string(data, '$.is_default') AS BOOLEAN) AS is_default,
    CAST(json_extract_string(data, '$.height') AS INTEGER) AS height,
    CAST(json_extract_string(data, '$.weight') AS INTEGER) AS weight,
    json_extract_string(data, '$.species.name') AS pokemon_species_name
FROM {{ source('staging', 'pokemon') }}
