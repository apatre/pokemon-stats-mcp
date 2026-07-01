WITH pivoted_stats AS (
    SELECT
        pokemon_name,
        MAX(CASE WHEN stat_name = 'hp' THEN base_stat END) AS stat_hp,
        MAX(CASE WHEN stat_name = 'attack' THEN base_stat END) AS stat_attack,
        MAX(CASE WHEN stat_name = 'defense' THEN base_stat END) AS stat_defense,
        MAX(CASE WHEN stat_name = 'special-attack' THEN base_stat END) AS stat_sp_attack,
        MAX(CASE WHEN stat_name = 'special-defense' THEN base_stat END) AS stat_sp_defense,
        MAX(CASE WHEN stat_name = 'speed' THEN base_stat END) AS stat_speed
    FROM {{ ref('pokemon__stats') }}
    GROUP BY 1
),
pokemon_types AS (
    SELECT
        pokemon_name,
        string_agg(type_name, '/') AS types
    FROM {{ ref('pokemon__type') }}
    GROUP BY 1
)
SELECT DISTINCT
    e.version_name,
    vg.version_group_name,
    l.location_name,
    l.location_area_name,
    e.pokemon_name,
    t.types AS pokemon_types,
    e.encounter_method,
    e.min_level,
    e.max_level,
    e.max_chance_per_version_name AS base_encounter_rate,
    e.chance_per_encounter_method AS method_encounter_rate,
    e.condition_values,
    s.stat_hp,
    s.stat_attack,
    s.stat_defense,
    s.stat_sp_attack,
    s.stat_sp_defense,
    s.stat_speed
FROM {{ ref('location_area__pokemon_encounters_rates') }} e
JOIN {{ ref('location') }} l ON e.location_area_name = l.location_area_name
LEFT JOIN {{ ref('versions') }} v ON e.version_name = v.version_name
LEFT JOIN {{ ref('version_groups') }} vg ON v.version_group_id = vg.version_group_id
LEFT JOIN pokemon_types t ON e.pokemon_name = t.pokemon_name
LEFT JOIN pivoted_stats s ON e.pokemon_name = s.pokemon_name
