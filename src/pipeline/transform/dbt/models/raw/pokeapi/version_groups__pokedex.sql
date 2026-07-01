WITH unnested AS (
    SELECT
        name AS version_group_name,
        json_extract_string(unnested_pokedex.val, '$.name') AS pokedex_name
    FROM {{ source('staging', 'version_group') }},
    LATERAL unnest(json_transform(json_extract(data, '$.pokedexes'), '["JSON"]')) AS unnested_pokedex(val)
)
SELECT
    md5(version_group_name || '_' || pokedex_name) AS sur_version_group_pokedex_name,
    version_group_name,
    pokedex_name
FROM unnested
