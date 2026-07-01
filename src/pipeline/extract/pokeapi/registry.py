from .base import BaseExtractor

class VersionGroupExtractor(BaseExtractor):
    api_name = "version-group"
    table_name = "version_group"

class VersionExtractor(BaseExtractor):
    api_name = "version"
    table_name = "version"

class RegionExtractor(BaseExtractor):
    api_name = "region"
    table_name = "region"

class LocationExtractor(BaseExtractor):
    api_name = "location"
    table_name = "location"

class LocationAreaExtractor(BaseExtractor):
    api_name = "location-area"
    table_name = "location_area"

class MoveLearnMethodExtractor(BaseExtractor):
    api_name = "move-learn-method"
    table_name = "move_learn_method"

class PokedexExtractor(BaseExtractor):
    api_name = "pokedex"
    table_name = "pokedex"

class PokemonSpeciesExtractor(BaseExtractor):
    api_name = "pokemon-species"
    table_name = "pokemon_species"

class PokemonExtractor(BaseExtractor):
    api_name = "pokemon"
    table_name = "pokemon"

class EvolutionChainExtractor(BaseExtractor):
    api_name = "evolution-chain"
    table_name = "evolution_chain"

class TypeExtractor(BaseExtractor):
    api_name = "type"
    table_name = "type"
