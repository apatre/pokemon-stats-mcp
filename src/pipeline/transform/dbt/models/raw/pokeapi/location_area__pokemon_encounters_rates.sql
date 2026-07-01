WITH unnested_encounters AS (
    SELECT
        id AS location_area_id,
        name AS location_area_name,
        json_extract_string(pe.val, '$.pokemon.name') AS pokemon_name,
        json_extract(pe.val, '$.version_details') AS version_details
    FROM {{ source('staging', 'location_area') }},
    LATERAL unnest(json_transform(json_extract(data, '$.pokemon_encounters'), '["JSON"]')) AS pe(val)
),
unnested_versions AS (
    SELECT
        location_area_id,
        location_area_name,
        pokemon_name,
        json_extract_string(vd.val, '$.version.name') AS version_name,
        CAST(json_extract_string(vd.val, '$.max_chance') AS INTEGER) AS max_chance_per_version_name,
        json_extract(vd.val, '$.encounter_details') AS encounter_details
    FROM unnested_encounters,
    LATERAL unnest(json_transform(version_details, '["JSON"]')) AS vd(val)
),
flat_details AS (
    SELECT
        location_area_id,
        location_area_name,
        pokemon_name,
        version_name,
        max_chance_per_version_name,
        json_extract_string(ed.val, '$.method.name') AS encounter_method,
        CAST(json_extract_string(ed.val, '$.min_level') AS INTEGER) AS min_level,
        CAST(json_extract_string(ed.val, '$.max_level') AS INTEGER) AS max_level,
        CAST(json_extract_string(ed.val, '$.chance') AS INTEGER) AS chance_per_encounter_method,
        json_extract_string(ed.val, '$.condition_values') AS condition_values_json
    FROM unnested_versions,
    LATERAL unnest(json_transform(encounter_details, '["JSON"]')) AS ed(val)
)
SELECT
    md5(location_area_id || '_' || pokemon_name || '_' || version_name || '_' || encounter_method || '_' || min_level || '_' || max_level) AS sur_location_area_pokemon_encounter_rate,
    location_area_id,
    encounter_method,
    pokemon_name,
    location_area_name,
    version_name,
    max_chance_per_version_name,
    min_level,
    max_level,
    (
        SELECT string_agg(json_extract_string(cond.val, '$.name'), ', ')
        FROM unnest(json_transform(condition_values_json, '["JSON"]')) AS cond(val)
    ) AS condition_values,
    chance_per_encounter_method
FROM flat_details
