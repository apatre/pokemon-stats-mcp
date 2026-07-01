WITH base_profile AS (
    SELECT
        pokemon_name,
        string_agg(CASE WHEN total_effectiveness = 4.0 THEN attacking_type END, ', ') AS quad_weaknesses,
        string_agg(CASE WHEN total_effectiveness = 2.0 THEN attacking_type END, ', ') AS double_weaknesses,
        string_agg(CASE WHEN total_effectiveness = 0.5 THEN attacking_type END, ', ') AS resistances,
        string_agg(CASE WHEN total_effectiveness = 0.25 THEN attacking_type END, ', ') AS quad_resistances,
        string_agg(CASE WHEN total_effectiveness = 0.0 THEN attacking_type END, ', ') AS immunities
    FROM {{ ref('pokemon_type_weaknesses') }}
    GROUP BY 1
),
pokemon_types AS (
    SELECT
        pokemon_name,
        string_agg(type_name, '/') AS types
    FROM {{ ref('pokemon__type') }}
    GROUP BY 1
)
SELECT
    p.pokemon_name,
    t.types AS pokemon_types,
    COALESCE(p.quad_weaknesses, 'None') AS quad_weaknesses,
    COALESCE(p.double_weaknesses, 'None') AS double_weaknesses,
    COALESCE(p.resistances, 'None') AS resistances,
    COALESCE(p.quad_resistances, 'None') AS quad_resistances,
    COALESCE(p.immunities, 'None') AS immunities
FROM base_profile p
LEFT JOIN pokemon_types t ON p.pokemon_name = t.pokemon_name
