import logging
from typing import Dict, Any
from pokemon_stats_mcp.database import DatabaseAdapter
from .pokeapi import (
    PokeAPIClient,
    VersionGroupExtractor,
    VersionExtractor,
    RegionExtractor,
    LocationExtractor,
    LocationAreaExtractor,
    MoveLearnMethodExtractor,
    PokedexExtractor,
    PokemonSpeciesExtractor,
    PokemonExtractor,
    EvolutionChainExtractor,
    TypeExtractor
)

logger = logging.getLogger("orchestration.extract")

def _extract_version_group_and_versions(
    version_group_name: str, 
    vg_ext: VersionGroupExtractor, 
    v_ext: VersionExtractor
) -> Dict[str, Any]:
    """Extract version group details and all associated versions."""
    logger.info(f"Extracting version group details: {version_group_name}")
    vg_data = vg_ext.extract_by_identifier(version_group_name)
    if not vg_data:
        raise ValueError(f"Version group '{version_group_name}' not found in source.")

    for ver in vg_data.get("versions", []):
        logger.info(f"Extracting version details: {ver['name']}")
        v_ext.extract_by_identifier(ver["name"])
        
    return vg_data


def _extract_types(type_ext: TypeExtractor) -> None:
    """Extract all Pokémon type definitions (global constant mapping)."""
    logger.info("Extracting all pokemon type definitions...")
    type_ext.extract_all(limit=20)


def _extract_regions_and_locations(
    vg_data: Dict[str, Any],
    reg_ext: RegionExtractor,
    loc_ext: LocationExtractor,
    la_ext: LocationAreaExtractor,
    limit: int
) -> None:
    """Extract regions and their locations/location-areas."""
    for reg in vg_data.get("regions", []):
        logger.info(f"Extracting region details: {reg['name']}")
        reg_data = reg_ext.extract_by_identifier(reg["name"])
        if reg_data:
            locations = reg_data.get("locations", [])
            for loc in locations[:limit]:
                logger.info(f"Extracting location: {loc['name']}")
                loc_data = loc_ext.extract_by_identifier(loc["name"])
                if loc_data:
                    for area in loc_data.get("areas", []):
                        la_ext.extract_by_identifier(area["name"])


def _extract_move_learn_methods(vg_data: Dict[str, Any], mlm_ext: MoveLearnMethodExtractor) -> None:
    """Extract move learn methods for the version group."""
    for mlm in vg_data.get("move_learn_methods", []):
        logger.info(f"Extracting move learn method: {mlm['name']}")
        mlm_ext.extract_by_identifier(mlm["name"])


def _extract_pokedexes_and_pokemon(
    vg_data: Dict[str, Any],
    pokedex_ext: PokedexExtractor,
    species_ext: PokemonSpeciesExtractor,
    ev_ext: EvolutionChainExtractor,
    pokemon_ext: PokemonExtractor,
    limit: int
) -> None:
    """Extract pokedexes and all their pokemon entries, including species, evolution, and varieties."""
    for pd in vg_data.get("pokedexes", []):
        logger.info(f"Extracting pokedex details: {pd['name']}")
        pd_data = pokedex_ext.extract_by_identifier(pd["name"])
        if pd_data:
            entries = pd_data.get("pokemon_entries", [])
            for entry in entries[:limit]:
                sp_name = entry.get("pokemon_species", {}).get("name")
                if sp_name:
                    logger.info(f"Extracting pokemon species: {sp_name}")
                    sp_data = species_ext.extract_by_identifier(sp_name)
                    if sp_data:
                        # Extract evolution chain
                        chain_url = sp_data.get("evolution_chain", {}).get("url")
                        if chain_url:
                            try:
                                chain_id = int(chain_url.rstrip("/").split("/")[-1])
                                ev_ext.extract_by_identifier(chain_id)
                            except Exception as ex:
                                logger.error(f"Error parsing chain ID from {chain_url}: {ex}")
                        
                        # Extract all pokemon varieties for this species
                        for var in sp_data.get("varieties", []):
                            p_name = var.get("pokemon", {}).get("name")
                            if p_name:
                                logger.info(f"Extracting pokemon details: {p_name}")
                                pokemon_ext.extract_by_identifier(p_name)


def extract_load(version_group_name: str, db_adapter: DatabaseAdapter, limit: int = 150) -> None:
    """Extract all resource data graph-traversal style and load into staging."""
    logger.info(f"Starting Extract-Load step for version group '{version_group_name}' (limit={limit})...")
    client = PokeAPIClient()
    
    # Instantiate all extractors
    vg_ext = VersionGroupExtractor(db_adapter, client)
    v_ext = VersionExtractor(db_adapter, client)
    reg_ext = RegionExtractor(db_adapter, client)
    loc_ext = LocationExtractor(db_adapter, client)
    la_ext = LocationAreaExtractor(db_adapter, client)
    mlm_ext = MoveLearnMethodExtractor(db_adapter, client)
    pokedex_ext = PokedexExtractor(db_adapter, client)
    species_ext = PokemonSpeciesExtractor(db_adapter, client)
    pokemon_ext = PokemonExtractor(db_adapter, client)
    ev_ext = EvolutionChainExtractor(db_adapter, client)
    type_ext = TypeExtractor(db_adapter, client)

    # Ensure all staging tables exist
    all_exts = [vg_ext, v_ext, reg_ext, loc_ext, la_ext, mlm_ext, pokedex_ext, species_ext, pokemon_ext, ev_ext, type_ext]
    for ext in all_exts:
        ext.create_table()

    # Step-by-step extraction
    vg_data = _extract_version_group_and_versions(version_group_name, vg_ext, v_ext)
    _extract_types(type_ext)
    _extract_regions_and_locations(vg_data, reg_ext, loc_ext, la_ext, limit)
    _extract_move_learn_methods(vg_data, mlm_ext)
    _extract_pokedexes_and_pokemon(vg_data, pokedex_ext, species_ext, ev_ext, pokemon_ext, limit)

    logger.info("Extract-Load step completed successfully!")
