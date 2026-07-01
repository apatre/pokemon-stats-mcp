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
    p.pokemon_id,
    p.pokemon_name,
    t.types,
    m.version_group_name,
    v.version_name,
    m.move_name,
    m.move_learn_method,
    m.level_learned_at,
    s.stat_hp,
    s.stat_attack,
    s.stat_defense,
    s.stat_sp_attack,
    s.stat_sp_defense,
    s.stat_speed
FROM {{ ref('pokemon') }} p
JOIN {{ ref('pokemon__move') }} m ON p.pokemon_name = m.pokemon_name
LEFT JOIN {{ ref('version_groups') }} vg ON m.version_group_name = vg.version_group_name
LEFT JOIN {{ ref('versions') }} v ON vg.version_group_id = v.version_group_id
LEFT JOIN pokemon_types t ON p.pokemon_name = t.pokemon_name
LEFT JOIN pivoted_stats s ON p.pokemon_name = s.pokemon_name
