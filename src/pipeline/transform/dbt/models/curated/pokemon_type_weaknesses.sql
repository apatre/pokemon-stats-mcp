WITH pokemon_types AS (
    SELECT
        pokemon_name,
        type_name
    FROM {{ ref('pokemon__type') }}
),
attacking_types AS (
    SELECT DISTINCT damage_type FROM {{ ref('type') }}
),
pokemon_attack_pairs AS (
    SELECT
        p.pokemon_name,
        a.damage_type
    FROM (SELECT DISTINCT pokemon_name FROM pokemon_types) p
    CROSS JOIN attacking_types a
),
individual_effectiveness AS (
    SELECT
        pa.pokemon_name,
        pa.damage_type,
        pt.type_name AS defender_type,
        COALESCE(r.damage_factor, 1.0) AS factor
    FROM pokemon_attack_pairs pa
    JOIN pokemon_types pt ON pa.pokemon_name = pt.pokemon_name
    LEFT JOIN {{ ref('type') }} r 
      ON pa.damage_type = r.damage_type 
     AND pt.type_name = r.target_type
)
SELECT
    pokemon_name,
    damage_type AS attacking_type,
    CASE 
        WHEN MIN(factor) = 0.0 THEN 0.0
        ELSE round(exp(sum(ln(CASE WHEN factor = 0.0 THEN 1.0 ELSE factor END))), 2)
    END AS total_effectiveness
FROM individual_effectiveness
GROUP BY 1, 2
