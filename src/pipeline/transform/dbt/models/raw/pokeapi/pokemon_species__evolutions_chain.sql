WITH base_chain AS (
    SELECT
        id AS evolution_chain_id,
        json_extract(data, '$.chain') AS chain
    FROM {{ source('staging', 'evolution_chain') }}
),
level_1 AS (
    SELECT
        evolution_chain_id,
        json_extract_string(chain, '$.species.name') AS pokemon_species_name,
        json_extract_string(l1.val, '$.species.name') AS evolves_to_species_name,
        json_extract_string(l1.val, '$.evolution_details[0].trigger.name') AS evolution_details_trigger_name,
        json_extract_string(l1.val, '$.evolution_details[0].gender') AS evolution_details_gender,
        json_extract_string(l1.val, '$.evolution_details[0].location.name') AS evolution_details_location,
        json_extract_string(l1.val, '$.evolution_details[0].min_level') AS evolution_details_min_level,
        json_extract_string(l1.val, '$.evolution_details[0].min_affection') AS evolution_details_min_affection,
        json_extract_string(l1.val, '$.evolution_details[0].time_of_day') AS evolution_detail_time_of_the_day,
        json_extract_string(l1.val, '$.evolution_details[0].trade_species.name') AS evolution_detail_trade_species,
        json_extract_string(l1.val, '$.evolution_details[0].region.name') AS evolution_detail_region,
        json_extract_string(l1.val, '$.evolution_details[0].min_moves') AS evolution_detail_min_move_count,
        json_extract_string(l1.val, '$.evolution_details[0].min_damage') AS evolution_detail_min_damage_taken,
        json_extract_string(l1.val, '$.evolution_details[0].min_steps') AS evolution_detail_min_steps
    FROM base_chain,
    LATERAL unnest(json_transform(json_extract(chain, '$.evolves_to'), '["JSON"]')) AS l1(val)
),
level_2 AS (
    SELECT
        c.id AS evolution_chain_id,
        json_extract_string(l1.val, '$.species.name') AS pokemon_species_name,
        json_extract_string(l2.val, '$.species.name') AS evolves_to_species_name,
        json_extract_string(l2.val, '$.evolution_details[0].trigger.name') AS evolution_details_trigger_name,
        json_extract_string(l2.val, '$.evolution_details[0].gender') AS evolution_details_gender,
        json_extract_string(l2.val, '$.evolution_details[0].location.name') AS evolution_details_location,
        json_extract_string(l2.val, '$.evolution_details[0].min_level') AS evolution_details_min_level,
        json_extract_string(l2.val, '$.evolution_details[0].min_affection') AS evolution_details_min_affection,
        json_extract_string(l2.val, '$.evolution_details[0].time_of_day') AS evolution_detail_time_of_the_day,
        json_extract_string(l2.val, '$.evolution_details[0].trade_species.name') AS evolution_detail_trade_species,
        json_extract_string(l2.val, '$.evolution_details[0].region.name') AS evolution_detail_region,
        json_extract_string(l2.val, '$.evolution_details[0].min_moves') AS evolution_detail_min_move_count,
        json_extract_string(l2.val, '$.evolution_details[0].min_damage') AS evolution_detail_min_damage_taken,
        json_extract_string(l2.val, '$.evolution_details[0].min_steps') AS evolution_detail_min_steps
    FROM {{ source('staging', 'evolution_chain') }} c,
    LATERAL unnest(json_transform(json_extract(c.data, '$.chain.evolves_to'), '["JSON"]')) AS l1(val),
    LATERAL unnest(json_transform(json_extract(l1.val, '$.evolves_to'), '["JSON"]')) AS l2(val)
),
combined AS (
    SELECT * FROM level_1
    UNION ALL
    SELECT * FROM level_2
)
SELECT
    md5(evolution_chain_id || '_' || pokemon_species_name || '_' || evolves_to_species_name) AS sur_evolution_chain_pokemon_species,
    *
FROM combined
