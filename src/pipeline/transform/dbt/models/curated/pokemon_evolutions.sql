SELECT DISTINCT
    s.pokemon_species_name,
    s.evolves_from_species,
    e.evolves_to_species_name AS next_evolution_species,
    e.evolution_details_trigger_name AS trigger_method,
    CASE 
        WHEN e.evolution_details_min_level IS NOT NULL AND e.evolution_details_min_level != '' 
        THEN CAST(e.evolution_details_min_level AS INTEGER) 
        ELSE NULL 
    END AS min_level,
    e.evolution_details_location AS location_required,
    e.evolution_detail_trade_species AS trade_pokemon_required,
    e.evolution_detail_time_of_the_day AS time_required,
    e.evolution_details_min_affection AS affection_required,
    e.evolution_detail_min_steps AS steps_required,
    CASE 
        WHEN e.evolution_details_trigger_name = 'level-up' AND (e.evolution_details_min_level IS NOT NULL AND e.evolution_details_min_level != '') 
            THEN 'Evolves to ' || e.evolves_to_species_name || ' at Level ' || e.evolution_details_min_level
        WHEN e.evolution_details_trigger_name = 'level-up' AND e.evolution_details_location IS NOT NULL 
            THEN 'Evolves to ' || e.evolves_to_species_name || ' by leveling up at ' || e.evolution_details_location
        WHEN e.evolution_details_trigger_name = 'level-up' AND e.evolution_details_min_affection IS NOT NULL 
            THEN 'Evolves to ' || e.evolves_to_species_name || ' by leveling up with high friendship'
        WHEN e.evolution_details_trigger_name = 'trade' AND e.evolution_detail_trade_species IS NOT NULL 
            THEN 'Evolves to ' || e.evolves_to_species_name || ' by trading for ' || e.evolution_detail_trade_species
        WHEN e.evolution_details_trigger_name = 'trade' 
            THEN 'Evolves to ' || e.evolves_to_species_name || ' by trading'
        WHEN e.evolution_details_trigger_name = 'use-item' 
            THEN 'Evolves to ' || e.evolves_to_species_name || ' by using an item'
        ELSE 'Evolves to ' || e.evolves_to_species_name || ' via ' || COALESCE(e.evolution_details_trigger_name, 'unknown method')
    END AS evolution_summary
FROM {{ ref('pokemon_species') }} s
LEFT JOIN {{ ref('pokemon_species__evolutions_chain') }} e 
  ON s.pokemon_species_name = e.pokemon_species_name
