SELECT DISTINCT
    pm.pokemon_name,
    pm.version_group_name,
    v.version_name,
    pm.move_learn_method,
    pm.level_learned_at,
    pm.move_name
FROM {{ ref('pokemon__move') }} pm
LEFT JOIN {{ ref('version_groups') }} vg ON pm.version_group_name = vg.version_group_name
LEFT JOIN {{ ref('versions') }} v ON vg.version_group_id = v.version_group_id
