SELECT
    id AS move_learn_method_id,
    name AS move_learn_method_name
FROM {{ source('staging', 'move_learn_method') }}
